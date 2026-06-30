"""FastAPI HTTP 서버 — 사용자 입력 수신 및 결과 조회."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

app = FastAPI(
    title="AI Career Copilot",
    description="멀티에이전트 + Kafka 기반 취업 준비 어시스턴트",
    version="0.1.0",
)

# TODO: web 서비스 origin을 환경변수로 분리
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
