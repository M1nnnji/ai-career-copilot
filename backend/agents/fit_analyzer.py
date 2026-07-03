"""
Fit Analyzer 에이전트
job.analyzed + resume.analyzed → fit.analyzed
"""

import json
import logging
from typing import Dict

from confluent_kafka import Consumer

from core.config import settings
from core.llm import call_llm_json, load_prompt
from core.result_store import save_error, save_result
from producers.events import publish_fit_analyzed

logger = logging.getLogger(__name__)

INPUT_TOPICS = [
    "job.analyzed",
    "resume.analyzed",
]

OUTPUT_TOPIC = "fit.analyzed"

_join_store: Dict[str, dict] = {}


def run_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": "fit-analyzer",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(INPUT_TOPICS)

    logger.info("Fit Analyzer started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        logger.info(msg.topic())
        logger.info("payload: %s", payload)
        
        try:
            topic = msg.topic()

            if topic == "job.analyzed":
                handle_partial(
                    payload["session_id"],
                    "job",
                    payload,
                )

            elif topic == "resume.analyzed":
                handle_partial(
                    payload["session_id"],
                    "resume",
                    payload,
                )

            consumer.commit(msg)

        except Exception as e:
            logger.exception("Fit Analyzer failed")
            if payload.get("session_id"):
                save_error(payload["session_id"], "fit", str(e))
            consumer.commit(msg)


def handle_partial(
    session_id: str,
    stage: str,
    data: dict,
):
    store = _join_store.setdefault(session_id, {})
    store[stage] = data

    if "job" not in store:
        return

    if "resume" not in store:
        return

    logger.info("Both results ready: %s", session_id)

    result = handle_joined(
        session_id,
        store["job"],
        store["resume"],
    )

    save_result(session_id, "fit", result)

    publish_fit_analyzed(
        session_id,
        result,
    )

    del _join_store[session_id]


def handle_joined(
    session_id: str,
    job_data: dict,
    resume_data: dict,
) -> dict:
    prompt = load_prompt("fit_analyzer")

    user_message = f"""
Job Analysis:
{job_data}

Resume Analysis:
{resume_data}
"""

    result = call_llm_json(
        prompt,
        user_message,
    )

    logger.info("LLM Result: %s", result)

    return result