"""
Fit Analyzer 에이전트 — job.analyzed + resume.analyzed 조인 → fit.analyzed 발행.
"""

import json
import logging
from typing import Dict

from confluent_kafka import Consumer

from core.config import settings
from producers.events import publish_fit_analyzed

logger = logging.getLogger(__name__)

INPUT_TOPICS = ("job.analyzed", "resume.analyzed")
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

    consumer.subscribe(list(INPUT_TOPICS))

    logger.info("Fit Analyzer started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        session_id = payload["session_id"]

        if msg.topic() == "job.analyzed":
            handle_partial(session_id, "job", payload)

        elif msg.topic() == "resume.analyzed":
            handle_partial(session_id, "resume", payload)

        consumer.commit(msg)


def handle_partial(session_id: str, stage: str, data: dict) -> None:
    _join_store.setdefault(session_id, {})[stage] = data

    if "job" not in _join_store[session_id]:
        return

    if "resume" not in _join_store[session_id]:
        return

    result = handle_joined(
        session_id,
        _join_store[session_id]["job"],
        _join_store[session_id]["resume"],
    )

    publish_fit_analyzed(session_id, result)

    _join_store.pop(session_id, None)


def handle_joined(session_id: str, job_data: dict, resume_data: dict) -> dict:
    logger.info("Both results ready: %s", session_id)

    return {
        "fit_score": 85,
        "strengths": [
            "Python",
            "FastAPI",
        ],
        "gaps": [
            "Docker",
        ],
    }