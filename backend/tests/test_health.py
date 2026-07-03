"""헬스체크 + 제출 API 테스트."""

import app.routes as routes
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    """GET /health → 200 ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


class _FakeDB:
    """SessionLocal() 대체 — DB 없이 add/commit no-op."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def add(self, obj):
        pass

    def commit(self):
        pass


def test_create_submission(monkeypatch):
    """이력서 없이 자소서만 제출하면 job/coverletter만 발행되고 resume는 생략."""
    published = []
    monkeypatch.setattr(routes, "SessionLocal", lambda: _FakeDB())
    monkeypatch.setattr(routes, "publish_job_submitted", lambda *a: published.append("job"))
    monkeypatch.setattr(routes, "publish_resume_submitted", lambda *a: published.append("resume"))
    monkeypatch.setattr(routes, "publish_coverletter_submitted", lambda *a: published.append("cover"))

    resp = client.post(
        "/submissions",
        json={
            "job_text": "Python backend engineer",
            "cover_letters": [{"question": "지원 동기", "draft": "초안입니다."}],
        },
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "submitted"
    assert "id" in body
    # 이력서 미제출 → resume 발행 안 됨.
    assert published == ["job", "cover"]


def test_create_submission_requires_cover_letters():
    """자소서 문항이 하나도 없으면 422 검증 오류."""
    resp = client.post(
        "/submissions",
        json={"job_text": "Python backend", "cover_letters": []},
    )
    assert resp.status_code == 422
