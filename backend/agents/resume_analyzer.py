"""
Resume Analyzer 에이전트 — resume.submitted 구독 → resume.analyzed 발행.
역할: 이력서에서 skills / projects JSON 추출.
"""

import logging

logger = logging.getLogger(__name__)

INPUT_TOPIC = "resume.submitted"
OUTPUT_TOPIC = "resume.analyzed"


def run_consumer():
    """Kafka consumer loop."""
    # TODO: confluent-kafka Consumer 생성, poll loop
    logger.info("Resume Analyzer consumer — TODO: implement")


def handle_message(payload: dict) -> dict:
    """
    TODO: prompts/resume_analyzer.txt → LLM → JSON → DB → produce
    """
    raise NotImplementedError("TODO: implement resume analysis")
