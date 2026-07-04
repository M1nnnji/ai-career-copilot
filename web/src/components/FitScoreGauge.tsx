/**
 * 적합도 점수 — fit_score 게이지 + strengths / gaps 태그.
 */
import type { FitAnalyzedResult } from "../types";

interface Props {
  fit: FitAnalyzedResult;
}

export default function FitScoreGauge({ fit }: Props) {
  const score = Math.max(0, Math.min(100, fit.fit_score));
  return (
    <div className="card">
      <h2>적합도</h2>

      <div className="fit-score-big" style={{ marginBottom: 10 }}>
        {score}
        <small> / 100</small>
      </div>
      <div className="score-track" style={{ marginBottom: 18 }}>
        <div className="score-fill big" style={{ width: `${score}%` }} />
      </div>

      <h3>강점</h3>
      <ul className="tag-list">
        {fit.strengths.map((s, i) => (
          <li key={i} className="tag strength">
            {s}
          </li>
        ))}
      </ul>

      <h3>부족 역량</h3>
      <ul className="tag-list">
        {fit.gaps.map((g, i) => (
          <li key={i} className="tag gap">
            {g}
          </li>
        ))}
      </ul>
    </div>
  );
}
