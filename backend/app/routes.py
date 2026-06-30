"""HTTP API 라우트 — 제출(submit)과 결과 조회(results)."""

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.database import get_db
from producers.events import (
    publish_coverletter_submitted,
    publish_job_submitted,
    publish_resume_submitted,
)
from schemas.events import SubmissionCreate, SubmissionResponse, ResultResponse

router = APIRouter()


@router.get("/health")
def health_check():
    """헬스체크 — docker-compose / 배포 확인용."""
    return {"status": "ok"}


@router.post("/submissions", response_model=SubmissionResponse)
def create_submission(payload: SubmissionCreate):
    """
    MVP 1단계:
    UUID 생성 → Kafka 토픽 발행 → 응답 반환
    (DB 저장은 다음 단계에서 구현)
    """

    submission_id = uuid4()

    publish_job_submitted(
        str(submission_id),
        payload.job_text,
    )

    publish_resume_submitted(
        str(submission_id),
        payload.resume_text,
    )

    publish_coverletter_submitted(
        str(submission_id),
        payload.cover_question,
        payload.cover_draft,
    )

    return SubmissionResponse(
        id=submission_id,
        status="submitted",
        created_at=datetime.now(),
    )


@router.get("/results/{submission_id}", response_model=ResultResponse)
def get_results(submission_id: UUID):
    """
    TODO: DB에서 분석 결과 조회
    """
    raise NotImplementedError("TODO: implement result polling")