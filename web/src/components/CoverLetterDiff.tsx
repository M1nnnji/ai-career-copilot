/**
 * 자소서 첨삭 결과(문항 1개) — 점수 + AI 작성 의심도 + issues + revised.
 */
import type { AiFlag, CoverLetterIssue, CoverLetterScores } from "../types";

interface Props {
  question: string;
  revised: string;
  issues: CoverLetterIssue[];
  scores?: CoverLetterScores;
  aiScore?: number;
  aiFlags?: AiFlag[];
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

function aiLevel(score: number): { label: string; color: string; bg: string } {
  if (score >= 70) return { label: "높음", color: "#991b1b", bg: "#fee2e2" };
  if (score >= 40) return { label: "보통", color: "#92400e", bg: "#fef3c7" };
  return { label: "낮음", color: "#166534", bg: "#dcfce7" };
}

export default function CoverLetterDiff({
  question,
  revised,
  issues,
  scores,
  aiScore,
  aiFlags,
}: Props) {
  const hasAi = typeof aiScore === "number";
  const lvl = hasAi ? aiLevel(aiScore as number) : null;

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

      {hasAi && lvl && (
        <div style={{ marginBottom: 16 }}>
          <h3>AI 작성 의심도</h3>
          <span
            className="badge"
            style={{ background: lvl.bg, color: lvl.color }}
          >
            {aiScore}/100 · {lvl.label}
          </span>
          <p className="field-hint" style={{ marginTop: 6 }}>
            회사가 AI로 쓴 티 나는 자소서를 감점할 수 있어요. 아래 표현을 본인 경험으로
            바꾸면 좋습니다.
          </p>
          {aiFlags && aiFlags.length > 0 && (
            <div>
              {aiFlags.map((f, i) => (
                <div key={i} className="issue">
                  <div className="issue-type">“{f.phrase}”</div>
                  <div className="issue-suggest">{f.reason}</div>
                </div>
              ))}
            </div>
          )}
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
