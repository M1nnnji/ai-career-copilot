"""
Kafka Worker 진입점
"""

import logging
from threading import Thread

from agents.fit_analyzer import run_consumer as run_fit_consumer
from agents.job_analyzer import run_consumer as run_job_consumer
from agents.resume_analyzer import run_consumer as run_resume_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting workers...")

    job_thread = Thread(target=run_job_consumer)
    resume_thread = Thread(target=run_resume_consumer)
    fit_thread = Thread(target=run_fit_consumer)

    job_thread.start()
    resume_thread.start()
    fit_thread.start()

    logger.info("Job Analyzer started.")
    logger.info("Resume Analyzer started.")
    logger.info("Fit Analyzer started.")

    job_thread.join()
    resume_thread.join()
    fit_thread.join()


if __name__ == "__main__":
    main()