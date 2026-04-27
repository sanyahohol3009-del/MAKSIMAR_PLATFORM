import React from "react";

import type { RightDrawerSection } from "../overlayDrawerLayoutContract.js";

type RightSystemContextDrawerProps = {
  isVisible: boolean;
  topStripHeight: number;
  drawerWidth: number;
  drawerOpacity: number;
  drawerBackdropBlurPx: number;
  activeRightSection: RightDrawerSection;
  rightDrawerSections: readonly RightDrawerSection[];
  onRightSectionChange: (section: RightDrawerSection) => void;
  getRightSectionTitle: (section: RightDrawerSection) => string;
  renderBody: () => React.ReactNode;
};

export function RightSystemContextDrawer({
  isVisible,
  topStripHeight,
  drawerWidth,
  drawerOpacity,
  drawerBackdropBlurPx,
  activeRightSection,
  rightDrawerSections,
  onRightSectionChange,
  getRightSectionTitle,
  renderBody,
}: RightSystemContextDrawerProps) {
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
        right: 0,
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
          <div className="view-switcher-group-title">Right Drawer</div>
          <div
            className="view-switcher"
            style={{
              display: "flex",
              flexWrap: "nowrap",
              overflowX: "auto",
              gap: 8,
            }}
          >
            {rightDrawerSections.map((section) => (
              <button
                key={section}
                type="button"
                className={
                  activeRightSection === section
                    ? "view-switch-button active"
                    : "view-switch-button"
                }
                onClick={() => onRightSectionChange(section)}
              >
                {getRightSectionTitle(section)}
              </button>
            ))}
          </div>
        </section>
      </div>

      {renderBody()}
    </aside>
  );
}
