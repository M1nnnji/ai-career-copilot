"""채용공고 URL 크롤링 — Playwright로 렌더링 후 본문 텍스트 추출."""

import logging
import re

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

# 본문일 가능성이 높은 영역 우선순위. 없으면 body로 폴백.
_MAIN_SELECTORS = ["main", "article", "[role='main']"]

# LLM 입력 폭주(지연·비용) 방지용 상한.
_MAX_CHARS = 6000


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
        finally:
            browser.close()

    cleaned = _clean(text)
    logger.info("Crawled text length: %d → %d", len(text), len(cleaned))
    return cleaned
