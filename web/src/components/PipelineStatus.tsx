/**
 * Kafka 파이프라인 진행 상태 — job → resume → fit → coverletter 스텝퍼.
 */
import type { ResultResponse, PipelineStage } from "../types";
import { PIPELINE_STAGES } from "../types";

interface Props {
  status: string;
  result: ResultResponse;
}

const LABELS: Record<PipelineStage, string> = {
  job: "공고 분석",
  resume: "이력서 분석",
  fit: "적합도",
  coverletter: "자소서 첨삭",
};

type StepState = "done" | "active" | "skipped" | "pending";

function isDone(result: ResultResponse, stage: PipelineStage): boolean {
  switch (stage) {
    case "job":
      return !!result.job;
    case "resume":
      return !!result.resume;
    case "fit":
      return !!result.fit;
    case "coverletter":
      return result.coverletters.length > 0;
  }
}

function isSkipped(result: ResultResponse, stage: PipelineStage): boolean {
  return (stage === "resume" || stage === "fit") && !result.resume_provided;
}

const ICON: Record<StepState, string> = {
  done: "✓",
  active: "",
  skipped: "–",
  pending: "·",
};
const STATE_LABEL: Record<StepState, string> = {
  done: "완료",
  active: "진행 중",
  skipped: "생략",
  pending: "대기",
};

export default function PipelineStatus({ status, result }: Props) {
  // 진행 중이면 '아직 안 끝났고 생략도 아닌' 첫 단계를 active로.
  const activeStage =
    status === "processing"
      ? PIPELINE_STAGES.find(
          (s) => !isDone(result, s) && !isSkipped(result, s)
        )
      : undefined;

  const stateOf = (stage: PipelineStage): StepState => {
    if (isDone(result, stage)) return "done";
    if (isSkipped(result, stage)) return "skipped";
    if (stage === activeStage) return "active";
    return "pending";
  };

  return (
    <div className="card">
      <h2>파이프라인</h2>
      <div className="stepper">
        {PIPELINE_STAGES.map((stage) => {
          const st = stateOf(stage);
          return (
            <div key={stage} className={`step ${st}`}>
              <div className="step-icon">
                {st === "active" ? <span className="spinner" /> : ICON[st]}
              </div>
              <div className="step-label">{LABELS[stage]}</div>
              <div className="step-state">{STATE_LABEL[st]}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
