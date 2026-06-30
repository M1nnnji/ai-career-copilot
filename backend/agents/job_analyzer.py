"""
Job Analyzer 에이전트 — job.submitted 구독 → job.analyzed 발행.
"""

import json
import logging

from confluent_kafka import Consumer

from core.config import settings
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

        payload = json.loads(msg.value().decode())

        result = handle_message(payload)

        publish_job_analyzed(
            payload["session_id"],
            result,
        )

        consumer.commit(msg)


def handle_message(payload: dict) -> dict:
    logger.info("Received job: %s", payload)

    return {
        "required_skills": [
            "Python",
            "FastAPI",
        ],
        "preferred_skills": [
            "Docker",
        ],
    }