/**
 * FastAPI 호출 클라이언트.
 * TODO: 환경변수 VITE_API_URL로 base URL 분리
 */

import type { SubmissionCreate, SubmissionResponse, ResultResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function createSubmission(
  payload: SubmissionCreate
): Promise<SubmissionResponse> {
  // TODO: POST /submissions 구현 후 연동
  const res = await fetch(`${API_BASE}/submissions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Submit failed: ${res.status}`);
  return res.json();
}

export async function getResults(submissionId: string): Promise<ResultResponse> {
  // TODO: polling으로 결과 조회 (GET /results/{id})
  const res = await fetch(`${API_BASE}/results/${submissionId}`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.status}`);
  return res.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
