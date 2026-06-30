-- MVP: submission 세션 + 단계별 분석 결과 저장
-- TODO: Alembic 대신 init.sql로 스키마 관리 (MVP 범위)

CREATE TABLE IF NOT EXISTS submissions (
    id          UUID PRIMARY KEY,
    status      VARCHAR(32) NOT NULL DEFAULT 'pending',
    job_text    TEXT,
    resume_text TEXT,
    cover_question TEXT,
    cover_draft    TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analysis_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id   UUID NOT NULL REFERENCES submissions(id),
    stage           VARCHAR(32) NOT NULL,  -- job | resume | fit | coverletter
    result_json     JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analysis_submission ON analysis_results(submission_id);
