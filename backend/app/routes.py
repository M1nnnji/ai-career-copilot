"""HTTP API 라우트 — 제출(submit)과 결과 조회(results)."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.events import SubmissionCreate, SubmissionResponse, ResultResponse

router = APIRouter()


@router.get("/health")
def health_check():
    """헬스체크 — docker-compose / 배포 확인용."""
    return {"status": "ok"}


@router.post("/submissions", response_model=SubmissionResponse)
def create_submission(payload: SubmissionCreate, db: Session = Depends(get_db)):
    """
    공고·이력서·자소서 입력 → DB 저장 → Kafka 토픽 발행.
    TODO: submission_service 로직 구현 (DB insert + producers.events 호출)
    """
    # TODO: UUID 생성, submissions 테이블 insert
    # TODO: job.submitted / resume.submitted / coverletter.submitted 발행
    raise NotImplementedError("TODO: implement submission flow")


@router.get("/results/{submission_id}", response_model=ResultResponse)
def get_results(submission_id: UUID, db: Session = Depends(get_db)):
    """
    세션별 분석·첨삭 결과 조회 — React polling용.
    TODO: submissions.status + analysis_results 조합하여 반환
    """
    raise NotImplementedError("TODO: implement result polling")
