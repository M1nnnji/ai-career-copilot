/**
 * 역량 커버리지 — 공고의 필수/우대 역량이 자소서에 언급됐는지 (ATS 키워드 매칭).
 */
import type { CoverageResult, SkillCoverage } from "../types";

interface Props {
  coverage: CoverageResult;
}

function SkillTags({ items }: { items: SkillCoverage[] }) {
  if (items.length === 0) return <p className="field-hint">추출된 역량이 없습니다.</p>;
  return (
    <ul className="tag-list">
      {items.map((s, i) => (
        <li key={i} className={`tag ${s.covered ? "strength" : "missing"}`}>
          {s.covered ? "✓" : "✗"} {s.skill}
        </li>
      ))}
    </ul>
  );
}

export default function CoverageCard({ coverage }: Props) {
  const reqPct = coverage.required_total
    ? Math.round((coverage.required_covered / coverage.required_total) * 100)
    : 0;

  return (
    <div className="card">
      <h2>역량 커버리지 · 자소서 기준</h2>
      <p className="field-hint">
        회사 서류 심사(ATS)는 공고의 역량 키워드가 지원서에 있는지를 봅니다. 자소서에
        언급된 역량과 빠진 역량이에요.
      </p>

      <h3>
        필수 역량 {coverage.required_covered}/{coverage.required_total} 커버 ({reqPct}%)
      </h3>
      <div className="score-track" style={{ margin: "6px 0 12px" }}>
        <div className="score-fill" style={{ width: `${reqPct}%` }} />
      </div>
      <SkillTags items={coverage.required} />

      <h3>
        우대 역량 {coverage.preferred_covered}/{coverage.preferred_total} 커버
      </h3>
      <SkillTags items={coverage.preferred} />
    </div>
  );
}
