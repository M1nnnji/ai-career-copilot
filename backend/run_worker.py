"""
Kafka Worker 진입점
"""

import logging

from agents.job_analyzer import run_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Job Analyzer consumer...")
    run_consumer()


if __name__ == "__main__":
    main()