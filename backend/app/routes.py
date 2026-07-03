"""HTTP API 라우트 — 제출(submit)과 결과 조회(results)."""

import logging
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from core.crawler import crawl_job
from core.database import SessionLocal
from core.result_store import get_result
from models.session import Submission
from producers.events import (
    publish_coverletter_submitted,
    publish_job_submitted,
    publish_resume_submitted,
)
from schemas.events import (
    SubmissionCreate,
    SubmissionResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check():
    """헬스체크"""
    return {"status": "ok"}


@router.post("/submissions", response_model=SubmissionResponse)
def create_submission(payload: SubmissionCreate):
    """
    UUID 생성 → 공고 크롤링(선택) → Kafka 발행
    """

    submission_id = uuid4()

    # URL이 들어오면 크롤링
    if payload.job_url:
        logger.info("Crawling job posting: %s", payload.job_url)

        try:
            job_text = crawl_job(payload.job_url)
        except Exception as e:
            logger.exception("Job crawling failed")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to crawl job url: {e}",
            )

    # 아니면 기존 방식
    elif payload.job_text:
        job_text = payload.job_text

    else:
        raise HTTPException(
            status_code=400,
            detail="job_text 또는 job_url 중 하나는 반드시 입력해야 합니다.",
        )

    # analysis_results가 FK로 참조하므로 submissions 행을 먼저 생성한다.
    with SessionLocal() as db:
        db.add(
            Submission(
                id=submission_id,
                status="submitted",
                job_text=job_text,
                resume_text=payload.resume_text,
                cover_question=payload.cover_question,
                cover_draft=payload.cover_draft,
            )
        )
        db.commit()

    publish_job_submitted(
        str(submission_id),
        job_text,
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


@router.get("/results/{submission_id}")
def get_results(submission_id: UUID):
    """
    메모리에 저장된 분석 결과 조회
    """

    stages = get_result(str(submission_id)) or {}

    # 자소서 첨삭까지 끝나면 완료, 아니면 아직 파이프라인 진행 중.
    status = "completed" if "coverletter" in stages else "processing"

    return {
        "id": str(submission_id),
        "status": status,
        "job": stages.get("job"),
        "resume": stages.get("resume"),
        "fit": stages.get("fit"),
        "coverletter": stages.get("coverletter"),
    }