"""FastAPI HTTP 서버 — 사용자 입력 수신 및 결과 조회."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.test_llm import router as test_router
from app.routes import router

app = FastAPI(
    title="AI Career Copilot",
    description="멀티에이전트 + Kafka 기반 취업 준비 어시스턴트",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    # 5174 = docker-compose가 web(5173)을 호스트로 매핑한 포트(브라우저 origin).
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(test_router)