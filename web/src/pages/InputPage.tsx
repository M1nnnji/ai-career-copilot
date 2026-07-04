/**
 * 입력 페이지 — 공고(필수) · 이력서(선택) · 자소서 다중 문항(필수).
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createSubmission } from "../api/client";
import type { CoverLetterInput } from "../types";

export default function InputPage() {
  const navigate = useNavigate();
  const [jobUrl, setJobUrl] = useState("");
  const [jobText, setJobText] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [coverLetters, setCoverLetters] = useState<CoverLetterInput[]>([
    { question: "", draft: "" },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateCover = (i: number, key: keyof CoverLetterInput, value: string) => {
    setCoverLetters((prev) =>
      prev.map((cl, idx) => (idx === i ? { ...cl, [key]: value } : cl))
    );
  };

  const addCover = () =>
    setCoverLetters((prev) => [...prev, { question: "", draft: "" }]);

  const removeCover = (i: number) =>
    setCoverLetters((prev) => prev.filter((_, idx) => idx !== i));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!jobUrl.trim() && !jobText.trim()) {
      setError("채용공고 URL 또는 텍스트 중 하나는 입력해야 합니다.");
      return;
    }
    const filled = coverLetters.filter(
      (cl) => cl.question.trim() && cl.draft.trim()
    );
    if (filled.length === 0) {
      setError("자소서 문항과 초안을 최소 1개는 입력해주세요.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await createSubmission({
        ...(jobUrl.trim() ? { job_url: jobUrl.trim() } : { job_text: jobText }),
        ...(resumeText.trim() ? { resume_text: resumeText } : {}),
        cover_letters: filled,
      });
      navigate(`/result/${res.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "제출 실패");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="page-title">채용공고 기준 자소서 첨삭</h1>
      <p className="page-lead">
        공고를 넣으면 요구 역량 기준으로 자소서를 문항별로 첨삭합니다. 이력서를 넣으면
        적합도 점수까지 분석해요.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="card">
          <h2>채용공고 *</h2>
          <input
            type="url"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            placeholder="채용공고 URL (입력 시 자동 크롤링)"
            style={{ marginBottom: 8 }}
          />
          <textarea
            rows={5}
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="또는 채용공고 텍스트를 직접 붙여넣으세요"
            disabled={!!jobUrl.trim()}
          />
        </div>

        <div className="card">
          <h2>이력서 (선택)</h2>
          <p className="field-hint">입력하면 공고 대비 적합도 점수까지 분석합니다.</p>
          <textarea
            rows={5}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="이력서 텍스트 (선택)"
          />
        </div>

        <div className="card">
          <h2>자소서 문항 *</h2>
          {coverLetters.map((cl, i) => (
            <div key={i} className="cover-item">
              <div className="cover-item-head">
                <input
                  type="text"
                  value={cl.question}
                  onChange={(e) => updateCover(i, "question", e.target.value)}
                  placeholder={`문항 ${i + 1} (예: 지원 동기를 작성하세요)`}
                />
                {coverLetters.length > 1 && (
                  <button
                    type="button"
                    className="btn btn-sm btn-danger-ghost"
                    onClick={() => removeCover(i)}
                  >
                    삭제
                  </button>
                )}
              </div>
              <textarea
                rows={5}
                value={cl.draft}
                onChange={(e) => updateCover(i, "draft", e.target.value)}
                placeholder="자소서 초안"
              />
            </div>
          ))}
          <button type="button" className="btn btn-ghost btn-sm" onClick={addCover}>
            + 문항 추가
          </button>
        </div>

        {error && <p className="error-text">{error}</p>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "제출 중..." : "분석 시작"}
        </button>
      </form>
    </div>
  );
}
