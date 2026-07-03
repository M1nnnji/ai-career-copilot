"""
결과 저장소 — PostgreSQL 기반.

API(uvicorn)와 Worker(run_worker)가 서로 다른 프로세스이므로
in-memory dict로는 결과를 공유할 수 없다. analysis_results 테이블에 저장해
양쪽이 같은 데이터를 보게 한다.
"""

import logging
import uuid

from sqlalchemy import select

from core.database import SessionLocal
from models.session import AnalysisResult, Submission

logger = logging.getLogger(__name__)


def _to_uuid(session_id) -> uuid.UUID:
    return session_id if isinstance(session_id, uuid.UUID) else uuid.UUID(str(session_id))


def save_result(session_id, stage: str, result: dict) -> None:
    """단계별 결과를 analysis_results 테이블에 저장."""
    with SessionLocal() as db:
        db.add(
            AnalysisResult(
                submission_id=_to_uuid(session_id),
                stage=stage,
                result_json=result,
            )
        )
        db.commit()

    logger.info("Saved result: session=%s stage=%s", session_id, stage)


def get_result(session_id):
    """
    세션의 모든 단계 결과를 {stage: result_json} 형태로 반환.
    결과가 하나도 없으면 None (→ 아직 processing).
    """
    with SessionLocal() as db:
        rows = (
            db.execute(
                select(AnalysisResult)
                .where(AnalysisResult.submission_id == _to_uuid(session_id))
                .order_by(AnalysisResult.created_at)
            )
            .scalars()
            .all()
        )

    if not rows:
        return None

    # 같은 stage가 여러 번 저장됐다면 created_at 오름차순 순회로 최신값이 남는다.
    return {row.stage: row.result_json for row in rows}


def mark_status(session_id, status: str) -> None:
    """submissions.status 갱신 (completed / failed 등)."""
    with SessionLocal() as db:
        sub = db.get(Submission, _to_uuid(session_id))
        if sub is not None:
            sub.status = status
            db.commit()

    logger.info("Status → %s: session=%s", status, session_id)


def save_error(session_id, stage: str, message: str) -> None:
    """에이전트 실패 기록 — error 단계로 저장하고 상태를 failed로 표시."""
    save_result(session_id, "error", {"stage": stage, "message": message})
    mark_status(session_id, "failed")
