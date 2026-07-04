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
import CoverageCard from "../components/CoverageCard";

const STATUS_LABEL: Record<string, string> = {
  processing: "분석 중",
  completed: "완료",
  failed: "실패",
};

export default function ResultPage() {
  const { submissionId } = useParams<{ submissionId: string }>();
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!submissionId) return;

    let timer: ReturnType<typeof setTimeout>;
    let cancelled = false;

    // 완료·실패 전까지 2.5초 간격으로 폴링.
    const poll = async () => {
      try {
        const data = await getResults(submissionId);
        if (cancelled) return;
        setResult(data);
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

  if (error) {
    return (
      <div className="page">
        <div className="banner error">{error}</div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="page">
        <div className="loading-wrap">
          <span className="spinner" /> 결과를 불러오는 중...
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          marginBottom: 4,
        }}
      >
        <h1 className="page-title" style={{ margin: 0 }}>
          분석 결과
        </h1>
        <span className={`badge ${result.status}`}>
          {result.status === "processing" && <span className="spinner" />}
          {STATUS_LABEL[result.status] ?? result.status}
        </span>
      </div>
      <p className="page-lead" style={{ fontSize: 13 }}>
        세션 {result.id}
      </p>

      {result.status === "failed" && result.error && (
        <div className="banner error">
          <strong>분석 실패 ({result.error.stage} 단계)</strong>
          <div style={{ marginTop: 4 }}>{result.error.message}</div>
        </div>
      )}

      <PipelineStatus status={result.status} result={result} />

      {result.status === "processing" && (
        <div className="loading-wrap" style={{ margin: "4px 2px 18px" }}>
          <span className="spinner" /> 분석이 진행 중입니다. 잠시만 기다려 주세요…
        </div>
      )}

      {result.fit && <FitScoreGauge fit={result.fit} />}

      {result.coverage && <CoverageCard coverage={result.coverage} />}

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
