/**
 * 앱 라우팅 + 상단 헤더.
 */
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import InputPage from "./pages/InputPage";
import ResultPage from "./pages/ResultPage";

export default function App() {
  return (
    <BrowserRouter>
      <header className="appbar">
        <div className="appbar-inner">
          <span className="appbar-logo">🎯</span>
          <Link
            to="/"
            style={{ textDecoration: "none", color: "inherit" }}
            className="appbar-title"
          >
            AI Career Copilot
          </Link>
          <span className="appbar-sub">· 서류합격 도우미</span>
        </div>
      </header>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/result/:submissionId" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}
