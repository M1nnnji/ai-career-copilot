"""
Fit Analyzer 에이전트 — job.analyzed + resume.analyzed 조인 → fit.analyzed 발행.
역할: 공고 요구사항 vs 이력서 비교 → fit_score / strengths / gaps.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

INPUT_TOPICS = ("job.analyzed", "resume.analyzed")
OUTPUT_TOPIC = "fit.analyzed"

# MVP: in-memory 조인 저장소 (session_id → {job?, resume?})
# TODO: 다중 worker / 재시작 내구성 필요 시 Redis로 교체
_join_store: Dict[str, dict] = {}


def run_consumer():
    """두 토픽을 구독하는 consumer loop."""
    # TODO: job.analyzed, resume.analyzed 각각 consumer 또는 하나의 consumer group
    logger.info("Fit Analyzer consumer — TODO: implement")


def handle_partial(session_id: str, stage: str, data: dict) -> None:
    """
    job 또는 resume 결과가 도착했을 때 조인 저장소에 적재.
    TODO: 둘 다 도착하면 handle_joined 호출
    """
    _join_store.setdefault(session_id, {})[stage] = data
    # TODO: job + resume 모두 있으면 handle_joined(session_id) 실행


def handle_joined(session_id: str, job_data: dict, resume_data: dict) -> dict:
    """
    TODO: prompts/fit_analyzer.txt → LLM → fit JSON → DB → fit.analyzed produce
    """
    raise NotImplementedError("TODO: implement fit analysis")
