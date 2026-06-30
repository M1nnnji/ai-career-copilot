/**
 * 입력 페이지 — 공고·이력서·자소서 텍스트 제출.
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createSubmission } from "../api/client";

export default function InputPage() {
  const navigate = useNavigate();
  const [jobText, setJobText] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [coverQuestion, setCoverQuestion] = useState("");
  const [coverDraft, setCoverDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // TODO: 입력 유효성 검사 (빈 값 방지)
      const res = await createSubmission({
        job_text: jobText,
        resume_text: resumeText,
        cover_question: coverQuestion,
        cover_draft: coverDraft,
      });
      navigate(`/result/${res.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "제출 실패");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <h1>AI Career Copilot</h1>
      <p>채용공고·이력서·자소서를 입력하면 Kafka 파이프라인으로 분석합니다.</p>

      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>채용공고</legend>
          <textarea
            rows={6}
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="채용공고 텍스트를 붙여넣으세요"
          />
        </fieldset>

        <fieldset>
          <legend>이력서</legend>
          <textarea
            rows={6}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="이력서 텍스트를 붙여넣으세요"
          />
        </fieldset>

        <fieldset>
          <legend>자소서</legend>
          <input
            type="text"
            value={coverQuestion}
            onChange={(e) => setCoverQuestion(e.target.value)}
            placeholder="문항 (예: 지원 동기를 작성하세요)"
            style={{ width: "100%", marginBottom: 8 }}
          />
          <textarea
            rows={6}
            value={coverDraft}
            onChange={(e) => setCoverDraft(e.target.value)}
            placeholder="자소서 초안"
          />
        </fieldset>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "제출 중..." : "분석 시작"}
        </button>
      </form>
    </div>
  );
}
