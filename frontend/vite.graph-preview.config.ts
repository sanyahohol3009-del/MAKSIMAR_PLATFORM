import { defineConfig } from "vite";
import path from "node:path";

export default defineConfig({
  root: path.resolve(__dirname, "react_flow_preview"),
  server: {
    host: "0.0.0.0",
    port: 4173,
  },
  preview: {
    host: "0.0.0.0",
    port: 4173,
  },
  build: {
    outDir: path.resolve(__dirname, "dist_react_flow_preview"),
    emptyOutDir: true,
  },
});
