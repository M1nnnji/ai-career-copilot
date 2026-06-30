"""
Cover Letter Editor 에이전트 — coverletter.submitted + fit.analyzed → coverletter.done.
역할: 구조·문장·직무적합 3관점 자소서 첨삭 (핵심 차별점).
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

INPUT_TOPICS = ("coverletter.submitted", "fit.analyzed")
OUTPUT_TOPIC = "coverletter.done"

# MVP: fit 결과 + 자소서 입력 조인 (session_id 기준)
_join_store: Dict[str, dict] = {}


def run_consumer():
    """coverletter.submitted, fit.analyzed 구독 consumer loop."""
    # TODO: 두 토픽 구독 및 조인 로직
    logger.info("Cover Letter Editor consumer — TODO: implement")


def handle_partial(session_id: str, stage: str, data: dict) -> None:
    """fit 또는 coverletter 입력이 도착했을 때 조인."""
    _join_store.setdefault(session_id, {})[stage] = data
    # TODO: fit + coverletter 모두 있으면 handle_joined 실행


def handle_joined(session_id: str, fit_data: dict, cover_data: dict) -> dict:
    """
    TODO: prompts/cover_letter_editor.txt → LLM → scores/issues/revised JSON
    TODO: DB 저장 → coverletter.done produce → submissions.status = complete
    """
    raise NotImplementedError("TODO: implement cover letter editing")
