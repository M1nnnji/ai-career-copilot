"""채용공고 URL 크롤링 — Playwright 렌더링 후 본문 텍스트 추출.

텍스트가 거의 없으면(JD가 이미지 한 장인 공고) 페이지를 스크린샷 찍어
Gemini 비전으로 텍스트를 추출한다. (텍스트 우선 + 비전 폴백)
"""

import logging
import re

from playwright.sync_api import sync_playwright

from core.llm import call_llm_vision

logger = logging.getLogger(__name__)

# 본문일 가능성이 높은 영역 우선순위. 없으면 body로 폴백.
_MAIN_SELECTORS = ["main", "article", "[role='main']"]

# LLM 입력 폭주(지연·비용) 방지용 상한.
_MAX_CHARS = 6000

# 이 글자 수 미만이면 '이미지 기반 공고'로 보고 비전 폴백.
_MIN_TEXT_CHARS = 400

_VISION_PROMPT = (
    "이 채용공고 페이지 이미지에서 보이는 모든 텍스트를 추출해줘. "
    "직무명, 담당 업무, 자격 요건, 우대 사항 등을 빠짐없이 그대로 옮겨줘. "
    "요약하거나 설명하지 말고 공고 본문 텍스트만 출력해."
)


def _clean(text: str) -> str:
    """과도한 공백/빈 줄 정리 후 길이 상한 적용."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > _MAX_CHARS:
        text = text[:_MAX_CHARS].rstrip() + "\n…(생략)"
    return text


def crawl_job(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # 본문 영역을 먼저 시도하고, 없으면 body 전체.
            text = ""
            for sel in _MAIN_SELECTORS:
                loc = page.locator(sel)
                if loc.count() > 0:
                    text = loc.first.inner_text()
                    logger.info("Crawled via selector: %s", sel)
                    break
            if not text.strip():
                text = page.locator("body").inner_text()
                logger.info("Crawled via body fallback")

            cleaned = _clean(text)

            # 텍스트가 거의 없으면 이미지 기반 공고 → 스크린샷 + 비전 추출.
            if len(cleaned) < _MIN_TEXT_CHARS:
                logger.info(
                    "Text too short (%d chars) — falling back to vision OCR",
                    len(cleaned),
                )
                shot = page.screenshot(full_page=True)
                vision_text = call_llm_vision(_VISION_PROMPT, shot, "image/png")
                cleaned = _clean(vision_text)
                logger.info("Vision extracted %d chars", len(cleaned))
        finally:
            browser.close()

    logger.info("Crawled text length: %d", len(cleaned))
    return cleaned
