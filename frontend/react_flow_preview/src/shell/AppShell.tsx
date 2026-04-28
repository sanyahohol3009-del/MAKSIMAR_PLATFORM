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

const permanentRailSlotStyle: React.CSSProperties = {
  position: "absolute",
  top: 0,
  left: 0,
  bottom: 0,
  zIndex: 12,
  pointerEvents: "auto",
};

const centerViewportSlotStyle: React.CSSProperties = {
  position: "absolute",
  top: 0,
  right: 0,
  bottom: 0,
  left: 104,
  zIndex: 1,
  minWidth: 0,
  overflow: "hidden",
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
      <main
        style={{
          ...overlayShellStyle,
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div
          className="permanent-dashboard-navigation-rail-slot"
          style={permanentRailSlotStyle}
          data-slot="left_permanent_navigation_rail_slot"
        >
          {permanentRail}
        </div>

        <div
          className="center-dashboard-viewport-slot"
          style={centerViewportSlotStyle}
          data-slot="center_dashboard_viewport_slot"
        >
          {centerViewport}
        </div>

        {topStatusStrip}
        {leftHandle}
        {rightHandle}
        {topChatDrawer}
        {summaryCardsOverlay}
        {leftDrawer}
        {rightDrawer}
      </main>

      {footer}
    </div>
  );
}
