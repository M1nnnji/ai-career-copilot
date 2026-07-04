/**
 * 자소서 첨삭 결과(문항 1개) — 문항 + 점수 바 + issues + revised.
 */
import type { CoverLetterIssue, CoverLetterScores } from "../types";

interface Props {
  question: string;
  revised: string;
  issues: CoverLetterIssue[];
  scores?: CoverLetterScores;
}

function ScoreBar({ name, value }: { name: string; value: number }) {
  const pct = Math.max(0, Math.min(5, value)) * 20;
  return (
    <div className="score-row">
      <span className="score-name">{name}</span>
      <span className="score-track">
        <span className="score-fill" style={{ width: `${pct}%` }} />
      </span>
      <span className="score-val">{value} / 5</span>
    </div>
  );
}

export default function CoverLetterDiff({ question, revised, issues, scores }: Props) {
  return (
    <div className="card">
      <h2>자소서 첨삭{question ? ` · ${question}` : ""}</h2>

      {scores && (
        <div style={{ marginBottom: 16 }}>
          <ScoreBar name="구조" value={scores.structure} />
          <ScoreBar name="명료성" value={scores.clarity} />
          <ScoreBar name="직무 적합" value={scores.job_fit} />
        </div>
      )}

      {issues.length > 0 && (
        <>
          <h3>개선 포인트</h3>
          {issues.map((issue, i) => (
            <div key={i} className="issue">
              <div className="issue-type">{issue.type}</div>
              <div>{issue.description}</div>
              {issue.suggestion && (
                <div className="issue-suggest">💡 {issue.suggestion}</div>
              )}
            </div>
          ))}
        </>
      )}

      <h3>개선안</h3>
      <p className="revised">{revised || "—"}</p>
    </div>
  );
}
