"""
Cover Letter Editor 에이전트
coverletter.submitted + fit.analyzed → coverletter.done
"""

import json
import logging
from typing import Dict

from confluent_kafka import Consumer

from core.config import settings
from core.llm import call_llm_json, load_prompt
from producers.events import publish_coverletter_done

logger = logging.getLogger(__name__)

INPUT_TOPICS = [
    "coverletter.submitted",
    "fit.analyzed",
]

OUTPUT_TOPIC = "coverletter.done"

_join_store: Dict[str, dict] = {}


def run_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": "coverletter-editor",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(INPUT_TOPICS)

    logger.info("Cover Letter Editor started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        try:
            session_id = payload["session_id"]

            if msg.topic() == "coverletter.submitted":
                handle_partial(
                    session_id,
                    "coverletter",
                    payload,
                )

            elif msg.topic() == "fit.analyzed":
                handle_partial(
                    session_id,
                    "fit",
                    payload,
                )

            consumer.commit(msg)

        except Exception:
            logger.exception("Cover Letter Editor failed")


def handle_partial(session_id: str, stage: str, data: dict):
    store = _join_store.setdefault(session_id, {})
    store[stage] = data

    if "fit" not in store:
        return

    if "coverletter" not in store:
        return

    logger.info("Both results ready: %s", session_id)

    result = handle_joined(
        session_id,
        store["fit"],
        store["coverletter"],
    )

    publish_coverletter_done(
        session_id,
        result,
    )

    del _join_store[session_id]


def handle_joined(
    session_id: str,
    fit_data: dict,
    cover_data: dict,
) -> dict:
    prompt = load_prompt("cover_letter_editor")

    user_message = f"""
Fit Analysis:
{fit_data}

Cover Letter:
{cover_data.get("coverletter_text", "")}
"""

    result = call_llm_json(
        prompt,
        user_message,
    )

    logger.info("LLM Result: %s", result)

    return result