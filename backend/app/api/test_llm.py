from fastapi import APIRouter

from core.llm import call_llm

router = APIRouter()


router = APIRouter(prefix="/test", tags=["test"])


@router.get("/llm")
def test_llm():
    result = call_llm(
        "너는 JSON만 반환하는 AI다.",
        """
다음 JSON만 반환해.

{
  "hello": "world"
}
""",
    )

    return {"response": result}