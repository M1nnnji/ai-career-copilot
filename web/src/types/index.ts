/**
 * 백엔드 schemas/events.py 와 1:1 대응하는 TypeScript 타입.
 */

export interface CoverLetterInput {
  question: string;
  draft: string;
}

export interface SubmissionCreate {
  job_text?: string;
  job_url?: string;
  resume_text?: string; // 선택 — 넣으면 적합도(fit)까지 분석
  cover_letters: CoverLetterInput[];
}

export interface SubmissionResponse {
  id: string;
  status: string;
  created_at: string;
}

export interface JobAnalyzedResult {
  required_skills: string[];
  preferred_skills: string[];
}

export interface ResumeAnalyzedResult {
  skills: string[];
  projects: string[];
}

export interface FitAnalyzedResult {
  fit_score: number;
  strengths: string[];
  gaps: string[];
}

export interface CoverLetterScores {
  structure: number;
  clarity: number;
  job_fit: number;
}

export interface CoverLetterIssue {
  type: string;
  description: string;
  suggestion: string;
}

export interface CoverLetterDoneResult {
  question: string;
  scores: CoverLetterScores;
  issues: CoverLetterIssue[];
  revised: string;
}

export interface SubmissionError {
  stage: string;
  message: string;
}

export interface ResultResponse {
  id: string;
  status: string; // processing | completed | failed
  resume_provided: boolean;
  job?: JobAnalyzedResult;
  resume?: ResumeAnalyzedResult;
  fit?: FitAnalyzedResult;
  coverletters: CoverLetterDoneResult[];
  error?: SubmissionError | null;
}

/** Kafka 파이프라인 단계 — PipelineStatus 컴포넌트용 */
export type PipelineStage = "job" | "resume" | "fit" | "coverletter";

export const PIPELINE_STAGES: PipelineStage[] = [
  "job",
  "resume",
  "fit",
  "coverletter",
];
