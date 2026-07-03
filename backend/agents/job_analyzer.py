"""
Job Analyzer 에이전트
job.submitted 구독 → job.analyzed 발행
"""

import json
import logging

from confluent_kafka import Consumer

from core.config import settings
from core.llm import call_llm_json, load_prompt
from core.result_store import save_result
from producers.events import publish_job_analyzed

logger = logging.getLogger(__name__)

INPUT_TOPIC = "job.submitted"
OUTPUT_TOPIC = "job.analyzed"


def run_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": "job-analyzer",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([INPUT_TOPIC])

    logger.info("Job Analyzer started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        try:
            payload = json.loads(msg.value().decode())

            result = handle_message(payload)

            save_result(payload["session_id"], "job", result)

            publish_job_analyzed(
                payload["session_id"],
                result,
            )

            consumer.commit(msg)

        except Exception:
            logger.exception("Job Analyzer failed")


def handle_message(payload: dict) -> dict:
    logger.info("Received job: %s", payload)

    prompt = load_prompt("job_analyzer")

    result = call_llm_json(
        prompt,
        payload["job_text"],
    )

    logger.info("LLM Result: %s", result)

    return result