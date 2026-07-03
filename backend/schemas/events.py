"""
Kafka 메시지 + HTTP API Pydantic 스키마 — 에이전트 간 JSON 계약.
모든 토픽 payload와 API 입출력의 단일 진실(source of truth).
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# --- Kafka 토픽 이름 상수 ---

TOPIC_JOB_SUBMITTED = "job.submitted"
TOPIC_JOB_ANALYZED = "job.analyzed"
TOPIC_RESUME_SUBMITTED = "resume.submitted"
TOPIC_RESUME_ANALYZED = "resume.analyzed"
TOPIC_FIT_ANALYZED = "fit.analyzed"
TOPIC_COVERLETTER_SUBMITTED = "coverletter.submitted"
TOPIC_COVERLETTER_DONE = "coverletter.done"


# --- 에이전트 출력 스키마 (명세서 JSON 예시) ---

class JobAnalyzedResult(BaseModel):
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


class ResumeAnalyzedResult(BaseModel):
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)


class FitAnalyzedResult(BaseModel):
    fit_score: int = 0
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class CoverLetterScores(BaseModel):
    structure: int = 0
    clarity: int = 0
    job_fit: int = 0


class CoverLetterIssue(BaseModel):
    type: str = ""
    description: str = ""
    suggestion: str = ""


class CoverLetterDoneResult(BaseModel):
    question: str = ""
    scores: CoverLetterScores = Field(default_factory=CoverLetterScores)
    issues: list[CoverLetterIssue] = Field(default_factory=list)
    revised: str = ""


# --- HTTP API ---

class CoverLetterInput(BaseModel):
    question: str
    draft: str


class SubmissionCreate(BaseModel):
    job_text: Optional[str] = None
    job_url: Optional[str] = None
    resume_text: Optional[str] = None  # 선택 — 넣으면 적합도(fit)까지 분석
    cover_letters: list[CoverLetterInput] = Field(min_length=1)


class SubmissionResponse(BaseModel):
    id: UUID
    status: str = "pending"
    created_at: datetime


class ResultResponse(BaseModel):
    id: UUID
    status: str
    job: Optional[JobAnalyzedResult] = None
    resume: Optional[ResumeAnalyzedResult] = None
    fit: Optional[FitAnalyzedResult] = None
    coverletters: list[CoverLetterDoneResult] = Field(default_factory=list)
