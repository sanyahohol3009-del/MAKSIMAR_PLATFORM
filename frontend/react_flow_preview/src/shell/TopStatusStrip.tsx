import React from "react";

type TopStatusStripProps = {
  title: string;
  isExpanded: boolean;
  topStripHeight: number;
  backdropBlurPx: number;
  onToggle: () => void;
};

export function TopStatusStrip({
  title,
  isExpanded,
  topStripHeight,
  backdropBlurPx,
  onToggle,
}: TopStatusStripProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: topStripHeight,
        zIndex: 50,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 16px",
        border: "none",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(10,16,34,0.22)",
        backdropFilter: `blur(${backdropBlurPx}px)`,
        color: "white",
        cursor: "pointer",
      }}
    >
      <span style={{ fontWeight: 700 }}>{title}</span>
      <span style={{ opacity: 0.72 }}>
        {isExpanded ? "▴" : "▾"}
      </span>
    </button>
  );
}
