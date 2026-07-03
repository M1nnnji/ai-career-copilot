/**
 * 자소서 첨삭 결과 — 점수 + issues(개선 포인트) + revised 개선안.
 */
import type { CoverLetterIssue, CoverLetterScores } from "../types";

interface Props {
  original: string;
  revised: string;
  issues: CoverLetterIssue[];
  scores?: CoverLetterScores;
}

export default function CoverLetterDiff({ original, revised, issues, scores }: Props) {
  return (
    <section>
      <h2>자소서 첨삭</h2>

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

      {original && (
        <div>
          <h3>원문</h3>
          <p>{original}</p>
        </div>
      )}

      <div>
        <h3>개선안</h3>
        <p style={{ whiteSpace: "pre-wrap" }}>{revised || "—"}</p>
      </div>
    </section>
  );
}
