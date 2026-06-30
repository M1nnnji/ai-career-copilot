/**
 * Kafka 파이프라인 진행 상태 — job → resume → fit → coverletter.
 */
import type { ResultResponse, PipelineStage } from "../types";
import { PIPELINE_STAGES } from "../types";

interface Props {
  status: string;
  result: ResultResponse;
}

function stageDone(result: ResultResponse, stage: PipelineStage): boolean {
  switch (stage) {
    case "job":
      return !!result.job;
    case "resume":
      return !!result.resume;
    case "fit":
      return !!result.fit;
    case "coverletter":
      return !!result.coverletter;
  }
}

export default function PipelineStatus({ status, result }: Props) {
  // TODO: D6에서 토픽 흐름 시각화 고도화 (애니메이션, 아이콘)
  return (
    <section>
      <h2>파이프라인</h2>
      <p>전체 상태: {status}</p>
      <ol>
        {PIPELINE_STAGES.map((stage) => (
          <li key={stage}>
            {stage}: {stageDone(result, stage) ? "완료" : "대기"}
          </li>
        ))}
      </ol>
    </section>
  );
}
