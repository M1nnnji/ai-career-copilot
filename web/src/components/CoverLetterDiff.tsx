/**
 * 자소서 첨삭 결과(문항 1개) — 문항 + 점수 + issues + revised 개선안.
 */
import type { CoverLetterIssue, CoverLetterScores } from "../types";

interface Props {
  question: string;
  revised: string;
  issues: CoverLetterIssue[];
  scores?: CoverLetterScores;
}

export default function CoverLetterDiff({ question, revised, issues, scores }: Props) {
  return (
    <section style={{ borderTop: "2px solid #eee", marginTop: 16, paddingTop: 8 }}>
      <h2>자소서 첨삭{question ? `: ${question}` : ""}</h2>

      {scores && (
        <ul>
          <li>구조: {scores.structure} / 5</li>
          <li>명료성: {scores.clarity} / 5</li>
          <li>직무 적합: {scores.job_fit} / 5</li>
        </ul>
      )}

      {issues.length > 0 && (
        <div>
          <h3>개선 포인트</h3>
          <ul>
            {issues.map((issue, i) => (
              <li key={i}>
                <strong>{issue.type}</strong>: {issue.description}
                {issue.suggestion && (
                  <div>
                    <em>제안: {issue.suggestion}</em>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div>
        <h3>개선안</h3>
        <p style={{ whiteSpace: "pre-wrap" }}>{revised || "—"}</p>
      </div>
    </section>
  );
}
