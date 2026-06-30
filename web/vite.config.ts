import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // TODO: API 프록시 필요 시 추가 — proxy: { "/api": "http://api:8000" }
  },
});
