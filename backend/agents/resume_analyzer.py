"""
Resume Analyzer 에이전트 — resume.submitted 구독 → resume.analyzed 발행.
"""

import json
import logging

from confluent_kafka import Consumer

from core.config import settings
from producers.events import publish_resume_analyzed

logger = logging.getLogger(__name__)

INPUT_TOPIC = "resume.submitted"
OUTPUT_TOPIC = "resume.analyzed"


def run_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": "resume-analyzer",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([INPUT_TOPIC])

    logger.info("Resume Analyzer started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        result = handle_message(payload)

        publish_resume_analyzed(
            payload["session_id"],
            result,
        )

        consumer.commit(msg)


def handle_message(payload: dict) -> dict:
    logger.info("Received resume: %s", payload)

    return {
        "skills": [
            "Python",
            "FastAPI",
        ],
        "projects": [
            "AI Career Copilot",
        ],
    }