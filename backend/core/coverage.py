"""JD 역량이 자소서에 언급됐는지 매칭 — ATS 키워드 커버리지.

회사 서류 심사(ATS)의 핵심 동작인 '키워드 매칭'을 그대로 흉내 낸다.
공고의 required/preferred 역량이 지원자 자소서 텍스트에 나타나는지 확인해,
'필수 N개 중 M개 커버 / 누락 스킬' 형태로 보여준다.
"""

import re


def _is_covered(skill: str, text: str) -> bool:
    """스킬이 텍스트에 언급됐는지 — 전체 문자열 또는 핵심 토큰(3자+) 매칭."""
    s = skill.strip().lower()
    if not s:
        return False

    t = text.lower()
    if s in t:
        return True

    # "REST API 설계" 같은 복합 스킬은 핵심 토큰으로 완화 매칭.
    # 3자 미만 토큰(설계/경험 등 일반어)은 오탐 방지를 위해 제외.
    for token in re.split(r"[\s/,·()]+", s):
        token = token.strip()
        if len(token) >= 3 and token in t:
            return True

    return False


def compute_coverage(
    required_skills: list[str],
    preferred_skills: list[str],
    text: str,
) -> dict:
    """필수/우대 역량별 커버 여부 + 요약 카운트."""
    req = [{"skill": s, "covered": _is_covered(s, text)} for s in required_skills]
    pref = [{"skill": s, "covered": _is_covered(s, text)} for s in preferred_skills]

    return {
        "required": req,
        "preferred": pref,
        "required_covered": sum(1 for x in req if x["covered"]),
        "required_total": len(req),
        "preferred_covered": sum(1 for x in pref if x["covered"]),
        "preferred_total": len(pref),
    }
