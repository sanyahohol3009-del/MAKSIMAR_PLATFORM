import React from "react";

type AppShellProps = {
  overlayShellStyle: React.CSSProperties;
  topStatusStrip: React.ReactNode;
  leftHandle: React.ReactNode;
  rightHandle: React.ReactNode;
  topChatDrawer: React.ReactNode;
  summaryCardsOverlay: React.ReactNode;
  permanentRail: React.ReactNode;
  centerViewport: React.ReactNode;
  leftDrawer: React.ReactNode;
  rightDrawer: React.ReactNode;
  footer: React.ReactNode;
};

export function AppShell({
  overlayShellStyle,
  topStatusStrip,
  leftHandle,
  rightHandle,
  topChatDrawer,
  summaryCardsOverlay,
  permanentRail,
  centerViewport,
  leftDrawer,
  rightDrawer,
  footer,
}: AppShellProps) {
  return (
    <div
      className="page-shell"
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <main style={overlayShellStyle}>
        {topStatusStrip}
        {leftHandle}
        {rightHandle}
        {topChatDrawer}
        {summaryCardsOverlay}
        {centerViewport}
        {leftDrawer}
        {rightDrawer}
      </main>

      {footer}
    </div>
  );
}
