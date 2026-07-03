"""
Cover Letter Editor 에이전트
coverletter.submitted + job.analyzed (+ fit.analyzed, 이력서 있을 때만)
→ 문항별 첨삭 → coverletter.done

이력서가 없으면 fit.analyzed는 오지 않으므로, coverletter.submitted의
has_resume 플래그로 무엇을 기다릴지 판단한다.
"""

import json
import logging
from typing import Dict, Optional

from confluent_kafka import Consumer

from core.config import settings
from core.llm import call_llm_json, load_prompt
from core.result_store import mark_status, save_error, save_result
from producers.events import publish_coverletter_done

logger = logging.getLogger(__name__)

INPUT_TOPICS = [
    "coverletter.submitted",
    "job.analyzed",
    "fit.analyzed",
]

OUTPUT_TOPIC = "coverletter.done"

_join_store: Dict[str, dict] = {}


def run_consumer():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": "coverletter-editor",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe(INPUT_TOPICS)

    logger.info("Cover Letter Editor started.")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        payload = json.loads(msg.value().decode())

        try:
            session_id = payload["session_id"]
            topic = msg.topic()

            if topic == "coverletter.submitted":
                handle_partial(session_id, "cover", payload)
            elif topic == "job.analyzed":
                handle_partial(session_id, "job", payload)
            elif topic == "fit.analyzed":
                handle_partial(session_id, "fit", payload)

            consumer.commit(msg)

        except Exception as e:
            logger.exception("Cover Letter Editor failed")
            if payload.get("session_id"):
                save_error(payload["session_id"], "coverletter", str(e))
            consumer.commit(msg)


def _ready(store: dict) -> bool:
    """첨삭을 시작할 수 있는지 — 자소서와 공고 분석은 필수, 적합도는 이력서 있을 때만."""
    if "cover" not in store or "job" not in store:
        return False
    if store["cover"].get("has_resume") and "fit" not in store:
        return False
    return True


def handle_partial(session_id: str, stage: str, data: dict):
    store = _join_store.setdefault(session_id, {})
    store[stage] = data

    if not _ready(store):
        return

    logger.info("Ready to edit cover letters: %s", session_id)

    cover = store["cover"]
    job_data = store["job"]
    fit_data = store.get("fit")  # 이력서 없으면 None

    results = []
    for item in cover["cover_letters"]:
        question = item.get("question", "")
        draft = item.get("draft", "")
        edited = handle_one(job_data, fit_data, question, draft)
        results.append({"question": question, **edited})

    logger.info("Saving %d cover letter result(s)...", len(results))

    save_result(session_id, "coverletter", results)
    mark_status(session_id, "completed")

    publish_coverletter_done(session_id, {"coverletters": results})

    del _join_store[session_id]


def handle_one(
    job_data: dict,
    fit_data: Optional[dict],
    question: str,
    draft: str,
) -> dict:
    prompt = load_prompt("cover_letter_editor")

    fit_section = f"\nJob Fit Analysis:\n{fit_data}\n" if fit_data else ""

    user_message = f"""
Job Requirements:
{job_data}
{fit_section}
Question:
{question}

Cover Letter Draft:
{draft}
"""

    result = call_llm_json(
        prompt,
        user_message,
    )

    logger.info("LLM Result (%s): %s", question, result)

    return result
