"""
메모리 기반 결과 저장소 (MVP)
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

_results: Dict[str, dict] = {}


def save_result(
    session_id: str,
    stage: str,
    result: dict,
):
    """
    결과 저장
    """
    _results.setdefault(session_id, {})
    _results[session_id][stage] = result

    logger.info(
        "Saved Result Store: %s",
        _results,
    )


def get_result(session_id: str):
    """
    결과 조회
    """
    logger.info(
        "Current Result Store: %s",
        _results,
    )

    return _results.get(session_id)