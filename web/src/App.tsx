/**
 * 앱 라우팅 — 입력 페이지 / 결과 페이지.
 */
import { BrowserRouter, Routes, Route } from "react-router-dom";
import InputPage from "./pages/InputPage";
import ResultPage from "./pages/ResultPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/result/:submissionId" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}
