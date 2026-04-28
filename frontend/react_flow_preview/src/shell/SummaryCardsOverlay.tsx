import React from "react";

type SummaryCardsOverlayProps = {
  isVisible: boolean;
  topStripHeight: number;
  activeViewTitle: string;
  nodeCountLabel: string;
  unreadCount: number;
  codeBlockCount: number;
  leftOffsetPx?: number;
};

export function SummaryCardsOverlay({
  isVisible,
  topStripHeight,
  activeViewTitle,
  nodeCountLabel,
  unreadCount,
  codeBlockCount,
  leftOffsetPx = 0,
}: SummaryCardsOverlayProps) {
  if (!isVisible) {
    return null;
  }

  const lightweightCardStyle: React.CSSProperties = {
    background: "rgba(255,255,255,0.018)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(255,255,255,0.07)",
    boxShadow: "0 10px 28px rgba(0,0,0,0.10)",
  };

  return (
    <>
      <div
        style={{
          position: "absolute",
          top: topStripHeight + 12,
          left: leftOffsetPx + 18,
          zIndex: 6,
          display: "grid",
          gap: 10,
          gridTemplateColumns: "repeat(2, minmax(130px, 1fr))",
          maxWidth: 340,
        }}
      >
        <div className="summary-card" style={lightweightCardStyle}>
          <span className="summary-label">Active View</span>
          <span className="summary-value">{activeViewTitle}</span>
        </div>

        <div className="summary-card" style={lightweightCardStyle}>
          <span className="summary-label">Nodes</span>
          <span className="summary-value">{nodeCountLabel}</span>
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: topStripHeight + 12,
          right: 18,
          zIndex: 6,
          display: "grid",
          gap: 10,
          gridTemplateColumns: "repeat(2, minmax(120px, 1fr))",
          width: 280,
          maxWidth: "calc(100% - 40px)",
        }}
      >
        <div className="summary-card" style={lightweightCardStyle}>
          <span className="summary-label">Unread</span>
          <span className="summary-value">{unreadCount}</span>
        </div>

        <div className="summary-card" style={lightweightCardStyle}>
          <span className="summary-label">Code Blocks</span>
          <span className="summary-value">{codeBlockCount}</span>
        </div>
      </div>
    </>
  );
}
