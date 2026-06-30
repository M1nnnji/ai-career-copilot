"""
Kafka Worker 진입점 — 4개 에이전트 consumer를 동시에 기동.
API와 분리된 프로세스로 실행 (docker-compose worker 서비스).
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # TODO: job_analyzer, resume_analyzer, fit_analyzer, cover_letter_editor
    #       각 consumer를 thread 또는 asyncio task로 기동
    logger.info("Worker starting — TODO: start agent consumers")
    raise NotImplementedError("TODO: implement worker startup")


if __name__ == "__main__":
    main()
