# AI Career Copilot

멀티에이전트 + Kafka 이벤트 드리븐 기반 취업 준비 어시스턴트 (MVP 포트폴리오)

## 무엇을 · 왜

- **문제**: 취준생이 공고·이력서·자소서를 각각 따로 준비하며 적합도와 첨삭을 일관되게 받기 어렵다.
- **해결**: 4개 AI 에이전트가 Kafka 토픽으로 연결되어 공고 분석 → 이력서 분석 → 적합도 → 자소서 첨삭을 자동 수행한다.

## 아키텍처 (TODO: 다이어그램 추가)

```
React → FastAPI(api) → Kafka → Worker(4 agents) → PostgreSQL → React(polling)
```

### Kafka 토픽 흐름

```
job.submitted      → Job Analyzer       → job.analyzed
resume.submitted   → Resume Analyzer    → resume.analyzed
(job + resume)     → Fit Analyzer       → fit.analyzed
coverletter.submitted + fit.analyzed → Cover Letter Editor → coverletter.done
```

## 프로젝트 구조

```
├── kafka/init-topics.sh    # 토픽 생성
├── postgres/init.sql       # DB 스키마
├── backend/
│   ├── app/                # FastAPI HTTP
│   ├── run_worker.py       # Kafka consumer 진입점
│   ├── agents/             # 4개 에이전트
│   ├── producers/          # Kafka 발행
│   ├── prompts/            # LLM 프롬프트
│   ├── core/               # config, db, llm
│   ├── schemas/            # JSON 계약
│   ├── models/             # ORM
│   └── tests/
└── web/                    # React 대시보드
```

## 실행법 (TODO: D1 완료 후 검증)

```bash
cp .env.example .env
# .env에 LLM API 키 입력

docker-compose up --build

# Kafka 토픽 생성 (최초 1회)
# TODO: init-topics.sh 실행 방법 문서화

# 접속
# Web:  http://localhost:5173
# API:  http://localhost:8000/docs
```

## 개발 일정 (명세서 기준)

| 일자 | 목표 |
|------|------|
| D1 | docker-compose + Kafka + Postgres 기동 |
| D2 | 입력 API → Job/Resume Analyzer |
| D3 | Fit Analyzer (토픽 조인) |
| D4 | Cover Letter Editor |
| D5 | 프롬프트 튜닝 |
| D6 | React 대시보드 |
| D7 | 에러 핸들링 · README · 데모 |

## TODO (현재 상태)

- [ ] Kafka 토픽 init 자동화
- [ ] Submission API + Kafka produce
- [ ] 4개 에이전트 consumer 구현
- [ ] LLM API 연동
- [ ] React polling 연동

## 트러블슈팅 & 회고

TODO: D7에서 작성
