"""
Kafka 이벤트 발행 — HTTP API에서 입력을 토픽으로 전달.
에이전트 handler에서 다음 단계 토픽 발행 시에도 사용.
"""
import json

from confluent_kafka import Producer
import logging
from typing import Any

from core.config import settings

logger = logging.getLogger(__name__)

# TODO: confluent-kafka Producer 싱글톤 초기화
_producer = None


def get_producer():
    """Kafka Producer 인스턴스 반환 (lazy init)."""
    global _producer

    if _producer is None:
        _producer = Producer(
            {
                "bootstrap.servers": settings.kafka_bootstrap_servers,
            }
        )

    return _producer


def publish(topic: str, key: str, value: dict[str, Any]) -> None:
    """공통 발행 함수"""

    producer = get_producer()

    producer.produce(
        topic=topic,
        key=key,
        value=json.dumps(value,  ensure_ascii=False),
    )

    producer.flush()

    logger.info("Published → topic=%s key=%s", topic, key)

# --- 토픽별 편의 함수 ---

def publish_job_submitted(session_id: str, job_text: str) -> None:
    publish("job.submitted", session_id, {"session_id": session_id, "job_text": job_text})


def publish_resume_submitted(session_id: str, resume_text: str) -> None:
    publish("resume.submitted", session_id, {"session_id": session_id, "resume_text": resume_text})


def publish_coverletter_submitted(
    session_id: str, cover_letters: list[dict], has_resume: bool
) -> None:
    publish(
        "coverletter.submitted",
        session_id,
        {
            "session_id": session_id,
            "cover_letters": cover_letters,
            "has_resume": has_resume,
        },
    )


def publish_job_analyzed(session_id: str, result: dict) -> None:
    publish("job.analyzed", session_id, {"session_id": session_id, **result})


def publish_resume_analyzed(session_id: str, result: dict) -> None:
    publish("resume.analyzed", session_id, {"session_id": session_id, **result})


def publish_fit_analyzed(session_id: str, result: dict) -> None:
    publish("fit.analyzed", session_id, {"session_id": session_id, **result})


def publish_coverletter_done(session_id: str, result: dict) -> None:
    publish("coverletter.done", session_id, {"session_id": session_id, **result})
