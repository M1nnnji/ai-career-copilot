/**
 * 백엔드 schemas/events.py 와 1:1 대응하는 TypeScript 타입.
 */

export interface SubmissionCreate {
  job_text?: string;
  job_url?: string;
  resume_text: string;
  cover_question: string;
  cover_draft: string;
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
  scores: CoverLetterScores;
  issues: CoverLetterIssue[];
  revised: string;
}

export interface ResultResponse {
  id: string;
  status: string;
  job?: JobAnalyzedResult;
  resume?: ResumeAnalyzedResult;
  fit?: FitAnalyzedResult;
  coverletter?: CoverLetterDoneResult;
}

/** Kafka 파이프라인 단계 — PipelineStatus 컴포넌트용 */
export type PipelineStage = "job" | "resume" | "fit" | "coverletter";

export const PIPELINE_STAGES: PipelineStage[] = [
  "job",
  "resume",
  "fit",
  "coverletter",
];
