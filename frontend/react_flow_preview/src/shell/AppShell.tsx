import React from "react";

import { VISIBLE_PERMANENT_RAIL_WIDTH_PX } from "../appShellPermanentRailLayoutOffsets.js";

type AppShellProps = {
  overlayShellStyle: React.CSSProperties;
  topReservedHeight: number;
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

function buildPermanentRailSlotStyle(
  topReservedHeight: number,
): React.CSSProperties {
  return {
    position: "absolute",
    top: topReservedHeight,
    left: 0,
    bottom: 0,
    width: VISIBLE_PERMANENT_RAIL_WIDTH_PX,
    zIndex: 12,
    pointerEvents: "auto",
  };
}

function buildCenterViewportSlotStyle(
  topReservedHeight: number,
): React.CSSProperties {
  return {
    position: "absolute",
    top: topReservedHeight,
    right: 0,
    bottom: 0,
    left: VISIBLE_PERMANENT_RAIL_WIDTH_PX,
    zIndex: 1,
    minWidth: 0,
    overflow: "hidden",
  };
}

export function AppShell({
  overlayShellStyle,
  topReservedHeight,
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
        {topStatusStrip}

        <div
          className="permanent-dashboard-navigation-rail-slot"
          style={buildPermanentRailSlotStyle(topReservedHeight)}
          data-slot="left_permanent_navigation_rail_slot"
        >
          {permanentRail}
        </div>

        <div
          className="center-dashboard-viewport-slot"
          style={buildCenterViewportSlotStyle(topReservedHeight)}
          data-slot="center_dashboard_viewport_slot"
        >
          {centerViewport}
        </div>

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
