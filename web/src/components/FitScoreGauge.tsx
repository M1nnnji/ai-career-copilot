/**
 * 적합도 점수 게이지 — fit_score / strengths / gaps 표시.
 */
import type { FitAnalyzedResult } from "../types";

interface Props {
  fit: FitAnalyzedResult;
}

export default function FitScoreGauge({ fit }: Props) {
  // TODO: D6에서 게이지 UI 고도화 (원형 차트 등)
  return (
    <section>
      <h2>적합도</h2>
      <p>
        <strong>{fit.fit_score}</strong> / 100
      </p>
      <div>
        <h3>강점</h3>
        <ul>
          {fit.strengths.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>부족 역량</h3>
        <ul>
          {fit.gaps.map((g) => (
            <li key={g}>{g}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
