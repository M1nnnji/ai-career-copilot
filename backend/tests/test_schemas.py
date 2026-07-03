"""Kafka 이벤트 스키마 + 발행 테스트."""

import json

import producers.events as events
from schemas.events import (
    CoverLetterDoneResult,
    FitAnalyzedResult,
    JobAnalyzedResult,
)


def test_job_analyzed_schema():
    data = JobAnalyzedResult(required_skills=["Java"], preferred_skills=["Kafka"])
    assert "Java" in data.required_skills


def test_fit_analyzed_schema():
    data = FitAnalyzedResult(fit_score=82, strengths=["Java"], gaps=["Docker"])
    assert data.fit_score == 82


def test_cover_letter_schema_defaults():
    data = CoverLetterDoneResult(question="지원 동기")
    assert data.question == "지원 동기"
    assert data.scores.job_fit == 0
    assert data.issues == []


class _FakeProducer:
    def __init__(self):
        self.captured = {}

    def produce(self, topic, key, value):
        self.captured.update(topic=topic, key=key, value=value)

    def flush(self):
        self.captured["flushed"] = True


def test_publish_job_submitted(monkeypatch):
    """publish_job_submitted → 올바른 토픽/키/payload로 produce + flush."""
    fake = _FakeProducer()
    monkeypatch.setattr(events, "get_producer", lambda: fake)

    events.publish_job_submitted("sid-123", "job posting text")

    assert fake.captured["topic"] == "job.submitted"
    assert fake.captured["key"] == "sid-123"
    assert fake.captured["flushed"] is True
    payload = json.loads(fake.captured["value"])
    assert payload["session_id"] == "sid-123"
    assert payload["job_text"] == "job posting text"
