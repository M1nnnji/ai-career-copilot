"""Kafka 이벤트 스키마 검증 테스트."""

import pytest

from schemas.events import (
    JobAnalyzedResult,
    ResumeAnalyzedResult,
    FitAnalyzedResult,
    CoverLetterDoneResult,
)


def test_job_analyzed_schema():
    data = JobAnalyzedResult(required_skills=["Java"], preferred_skills=["Kafka"])
    assert "Java" in data.required_skills


def test_fit_analyzed_schema():
    data = FitAnalyzedResult(fit_score=82, strengths=["Java"], gaps=["Docker"])
    assert data.fit_score == 82


@pytest.mark.skip(reason="TODO: producer mock 후 publish 테스트 추가")
def test_publish_job_submitted():
    pass
