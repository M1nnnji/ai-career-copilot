"""
Cover Letter Editor 에이전트 — coverletter.submitted + fit.analyzed → coverletter.done.
"""

import json
import logging
from typing import Dict

from confluent_kafka import Consumer

from core.config import settings
from producers.events import publish_coverletter_done

logger = logging.getLogger(__name__)

INPUT_TOPICS = ("coverletter.submitted", "fit.analyzed")
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

    consumer.subscribe(list(INPUT_TOPICS))

    logger.info("Cover Letter Editor started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        session_id = payload["session_id"]

        if msg.topic() == "coverletter.submitted":
            handle_partial(session_id, "coverletter", payload)

        elif msg.topic() == "fit.analyzed":
            handle_partial(session_id, "fit", payload)

        consumer.commit(msg)


def handle_partial(session_id: str, stage: str, data: dict) -> None:
    _join_store.setdefault(session_id, {})[stage] = data

    if "fit" not in _join_store[session_id]:
        return

    if "coverletter" not in _join_store[session_id]:
        return

    result = handle_joined(
        session_id,
        _join_store[session_id]["fit"],
        _join_store[session_id]["coverletter"],
    )

    publish_coverletter_done(session_id, result)

    _join_store.pop(session_id, None)


def handle_joined(session_id: str, fit_data: dict, cover_data: dict) -> dict:
    logger.info("Both results ready: %s", session_id)

    return {
        "scores": {
            "structure": 90,
            "clarity": 88,
            "fit": 85,
        },
        "issues": [
            "Docker 경험을 조금 더 강조하세요."
        ],
        "revised": "수정된 자기소개서 예시입니다."
    }