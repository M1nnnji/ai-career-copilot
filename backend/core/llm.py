"""
LLM 클라이언트 래퍼 — Gemini API 호출 및 JSON 파싱.
"""

import json
import logging
import time
from pathlib import Path

from google import genai

from core.config import settings

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

client = genai.Client(api_key=settings.gemini_api_key)


def load_prompt(agent_name: str) -> str:
    """prompts/{agent_name}.txt 파일 로드."""
    path = PROMPTS_DIR / f"{agent_name}.txt"

    if not path.exists():
        logger.warning("Prompt file not found: %s", path)
        return ""

    return path.read_text(encoding="utf-8")


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Gemini API 호출 — raw text 반환.
    """

    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
{system_prompt}

------------------------
USER INPUT

{user_message}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return response.text.strip()

        except Exception as e:
            logger.warning(
                "Gemini request failed (%d/3): %s",
                attempt + 1,
                e,
            )

            if attempt == 2:
                raise

            time.sleep(2)


def call_llm_json(
    system_prompt: str,
    user_message: str,
    max_retries: int = 2,
) -> dict:
    """
    JSON 구조화 출력.
    """

    for attempt in range(max_retries + 1):

        try:
            text = call_llm(system_prompt, user_message)

            text = text.strip()

            if text.startswith("```json"):
                text = (
                    text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            return json.loads(text)

        except json.JSONDecodeError:
            logger.warning(
                "JSON parse failed (%d/%d)",
                attempt + 1,
                max_retries + 1,
            )

        except Exception as e:
            logger.warning(
                "LLM request failed (%d/%d): %s",
                attempt + 1,
                max_retries + 1,
                e,
            )

        if attempt < max_retries:
            time.sleep(2)

    raise ValueError("LLM did not return valid JSON.")