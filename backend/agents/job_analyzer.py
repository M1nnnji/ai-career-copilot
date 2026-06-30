"""
Job Analyzer 에이전트 — job.submitted 구독 → job.analyzed 발행.
역할: 채용공고에서 required/preferred skills JSON 추출.
"""

import logging

logger = logging.getLogger(__name__)

INPUT_TOPIC = "job.submitted"
OUTPUT_TOPIC = "job.analyzed"


def run_consumer():
    """Kafka consumer loop — 메시지 수신 후 handle_message 호출."""
    # TODO: confluent-kafka Consumer 생성, poll loop
    logger.info("Job Analyzer consumer — TODO: implement")


def handle_message(payload: dict) -> dict:
    """
    단일 메시지 처리.
    TODO: prompts/job_analyzer.txt 로드 → core.llm 호출 → JSON 파싱 → DB 저장 → produce
    """
    raise NotImplementedError("TODO: implement job analysis")
