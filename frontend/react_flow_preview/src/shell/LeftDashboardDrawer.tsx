import React from "react";

import type { LeftDrawerSection } from "../overlayDrawerLayoutContract.js";

type LeftDashboardDrawerProps = {
  isVisible: boolean;
  topStripHeight: number;
  drawerWidth: number;
  drawerOpacity: number;
  drawerBackdropBlurPx: number;
  activeLeftSection: LeftDrawerSection;
  leftDrawerSections: readonly LeftDrawerSection[];
  onLeftSectionChange: (section: LeftDrawerSection) => void;
  getLeftSectionTitle: (section: LeftDrawerSection) => string;
  renderBody: () => React.ReactNode;
};

export function LeftDashboardDrawer({
  isVisible,
  topStripHeight,
  drawerWidth,
  drawerOpacity,
  drawerBackdropBlurPx,
  activeLeftSection,
  leftDrawerSections,
  onLeftSectionChange,
  getLeftSectionTitle,
  renderBody,
}: LeftDashboardDrawerProps) {
  if (!isVisible) {
    return null;
  }

  return (
    <aside
      style={{
        position: "absolute",
        zIndex: 20,
        top: topStripHeight,
        bottom: 16,
        left: 0,
        width: drawerWidth,
        opacity: drawerOpacity,
        border: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(10, 16, 34, 0.34)",
        backdropFilter: `blur(${drawerBackdropBlurPx}px)`,
        boxShadow: "0 20px 60px rgba(0,0,0,0.18)",
        overflow: "auto",
        padding: "16px 14px 18px 14px",
      }}
    >
      <div className="view-switcher-group-shell">
        <section className="view-switcher-group">
          <div className="view-switcher-group-title">Left Drawer</div>
          <div
            className="view-switcher"
            style={{
              display: "flex",
              flexWrap: "nowrap",
              overflowX: "auto",
              gap: 8,
            }}
          >
            {leftDrawerSections.map((section) => (
              <button
                key={section}
                type="button"
                className={
                  activeLeftSection === section
                    ? "view-switch-button active"
                    : "view-switch-button"
                }
                onClick={() => onLeftSectionChange(section)}
              >
                {getLeftSectionTitle(section)}
              </button>
            ))}
          </div>
        </section>
      </div>

      {renderBody()}
    </aside>
  );
}
