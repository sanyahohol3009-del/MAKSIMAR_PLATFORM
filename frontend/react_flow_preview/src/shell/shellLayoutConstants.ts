import type { CSSProperties } from "react";

export const SHELL_TOP_STRIP_HEIGHT_PX = 42;

export const SHELL_MAIN_VISUAL_HEIGHT = "78vh";

export const SHELL_OVERLAY_STYLE: CSSProperties = {
  position: "relative",
  height: SHELL_MAIN_VISUAL_HEIGHT,
  borderRadius: 24,
  overflow: "hidden",
  border: "1px solid rgba(255,255,255,0.08)",
  background:
    "radial-gradient(circle at center, rgba(22,36,72,0.32), rgba(6,10,24,0.96))",
};
