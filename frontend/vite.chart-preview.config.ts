import { defineConfig } from "vite";
import path from "node:path";

export default defineConfig({
  root: path.resolve(__dirname, "react_flow_preview"),
  server: {
    host: "0.0.0.0",
    port: 4174,
  },
  preview: {
    host: "0.0.0.0",
    port: 4174,
  },
  build: {
    rollupOptions: {
      input: {
        chart_preview: path.resolve(__dirname, "react_flow_preview/chart_preview.html"),
      },
    },
    outDir: path.resolve(__dirname, "dist_chart_preview"),
    emptyOutDir: true,
  },
});
