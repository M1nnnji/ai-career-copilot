/**
 * 결과 페이지 — 적합도·첨삭 결과 + 파이프라인 진행 상태 (polling).
 */
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getResults } from "../api/client";
import type { ResultResponse } from "../types";
import FitScoreGauge from "../components/FitScoreGauge";
import CoverLetterDiff from "../components/CoverLetterDiff";
import PipelineStatus from "../components/PipelineStatus";

export default function ResultPage() {
  const { submissionId } = useParams<{ submissionId: string }>();
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!submissionId) return;

    let timer: ReturnType<typeof setTimeout>;
    let cancelled = false;

    // completed가 될 때까지 2.5초 간격으로 폴링.
    const poll = async () => {
      try {
        const data = await getResults(submissionId);
        if (cancelled) return;
        setResult(data);
        // 완료·실패 전까지 계속 폴링.
        if (data.status !== "completed" && data.status !== "failed") {
          timer = setTimeout(poll, 2500);
        }
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "조회 실패");
      }
    };

    poll();

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [submissionId]);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!result) return <p>결과를 불러오는 중...</p>;

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <h1>분석 결과</h1>
      <p>세션 ID: {result.id}</p>
      <p>상태: {result.status}</p>

      {result.status === "failed" && result.error && (
        <div
          style={{
            border: "1px solid #e00",
            background: "#fee",
            borderRadius: 6,
            padding: 12,
            marginBottom: 12,
            color: "#900",
          }}
        >
          <strong>분석 실패 ({result.error.stage} 단계)</strong>
          <p style={{ margin: "4px 0 0" }}>{result.error.message}</p>
        </div>
      )}

      <PipelineStatus status={result.status} result={result} />

      {result.fit && <FitScoreGauge fit={result.fit} />}

      {result.coverletters.map((cl, i) => (
        <CoverLetterDiff
          key={i}
          question={cl.question}
          revised={cl.revised}
          issues={cl.issues}
          scores={cl.scores}
        />
      ))}
    </div>
  );
}
