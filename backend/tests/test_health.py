"""헬스체크 API 테스트."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """GET /health → 200 ok."""
    # TODO: routes 구현 후 실제 assertion 활성화
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.skip(reason="TODO: submission flow 구현 후 활성화")
def test_create_submission():
    """POST /submissions — 입력 → session_id 반환."""
    pass
