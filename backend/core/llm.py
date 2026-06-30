"""
LLM 클라이언트 래퍼 — Claude / OpenAI API 호출 및 JSON 파싱.
TODO: D2~D5에서 실제 API 연동 및 재시도 로직 구현.
"""

import logging
from pathlib import Path

from core.config import settings

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(agent_name: str) -> str:
    """prompts/{agent_name}.txt 파일 로드."""
    path = PROMPTS_DIR / f"{agent_name}.txt"
    # TODO: 파일 없을 때 명확한 에러 처리
    if not path.exists():
        logger.warning("Prompt file not found: %s", path)
        return ""
    return path.read_text(encoding="utf-8")


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    LLM API 호출 — raw text 반환.
    TODO: settings.llm_provider에 따라 OpenAI / Anthropic 분기
    TODO: API 키 미설정 시 명확한 에러
    """
    raise NotImplementedError("TODO: implement LLM API call")


def call_llm_json(system_prompt: str, user_message: str, max_retries: int = 1) -> dict:
    """
    JSON 구조화 출력 — 파싱 실패 시 max_retries만큼 재요청.
    TODO: json.loads + Pydantic 검증
    """
    raise NotImplementedError("TODO: implement JSON LLM call with retry")
