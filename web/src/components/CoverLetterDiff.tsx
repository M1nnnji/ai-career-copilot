/**
 * 자소서 첨삭 전후 비교 — issues + revised 문단.
 */
interface Props {
  original: string;
  revised: string;
  issues: string[];
}

export default function CoverLetterDiff({ original, revised, issues }: Props) {
  // TODO: D6에서 side-by-side diff UI
  return (
    <section>
      <h2>자소서 첨삭</h2>

      {issues.length > 0 && (
        <div>
          <h3>개선 포인트</h3>
          <ul>
            {issues.map((issue, i) => (
              <li key={i}>{issue}</li>
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
        <p>{revised || "—"}</p>
      </div>
    </section>
  );
}
