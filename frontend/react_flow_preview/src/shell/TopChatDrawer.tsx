import React from "react";

import type { JarvisChatDrawerSectionId } from "../jarvis_chat/jarvisChatDrawerContract.js";
import type { EmbeddedChatSurfaceId } from "../jarvis_chat/embeddedChatSurfaceRegistry.js";

type TopDrawerExposureRow = {
  surfaceId: EmbeddedChatSurfaceId;
  title: string;
  countLabel: string;
  countValue: number;
};

type TopDrawerExposureGroup = {
  rows: readonly TopDrawerExposureRow[];
} | null;

type TopChatDrawerProps = {
  isOpen: boolean;
  topStripHeight: number;
  overlayOpacity: number;
  backdropBlurPx: number;
  compactHeaderSpacing: boolean;
  showSectionTabs: boolean;
  showSurfaceSelector: boolean;
  collapseSurfaceSelector: boolean;
  showSummaryChipLane: boolean;
  collapseSummaryChipLane: boolean;
  showSupportMeta: boolean;
  contentDominant: boolean;
  topCommunicationDensityMode: string;
  activeJarvisChatSection: JarvisChatDrawerSectionId;
  activeEmbeddedChatSurface: EmbeddedChatSurfaceId;
  jarvisChatSections: readonly JarvisChatDrawerSectionId[];
  topDrawerExposureGroup: TopDrawerExposureGroup;
  onJarvisChatSectionChange: (section: JarvisChatDrawerSectionId) => void;
  onEmbeddedChatSurfaceChange: (surfaceId: EmbeddedChatSurfaceId) => void;
  getJarvisChatSectionTitle: (
    section: JarvisChatDrawerSectionId,
  ) => string;
  renderTopDrawerBody: () => React.ReactNode;
};

export function TopChatDrawer({
  isOpen,
  topStripHeight,
  overlayOpacity,
  backdropBlurPx,
  compactHeaderSpacing,
  showSectionTabs,
  showSurfaceSelector,
  collapseSurfaceSelector,
  showSummaryChipLane,
  collapseSummaryChipLane,
  showSupportMeta,
  contentDominant,
  topCommunicationDensityMode,
  activeJarvisChatSection,
  activeEmbeddedChatSurface,
  jarvisChatSections,
  topDrawerExposureGroup,
  onJarvisChatSectionChange,
  onEmbeddedChatSurfaceChange,
  getJarvisChatSectionTitle,
  renderTopDrawerBody,
}: TopChatDrawerProps) {
  if (!isOpen) {
    return null;
  }

  return (
    <section
      style={{
        position: "absolute",
        top: topStripHeight,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 45,
        opacity: overlayOpacity,
        border: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(10, 16, 34, 0.34)",
        backdropFilter: `blur(${backdropBlurPx}px)`,
        boxShadow: "0 20px 60px rgba(0,0,0,0.18)",
        overflow: "auto",
        padding: "18px 20px 22px 20px",
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateRows: "auto auto auto 1fr",
          gap: compactHeaderSpacing ? 10 : 14,
          height: "100%",
        }}
      >
        {showSectionTabs ? (
          <section className="view-switcher-group">
            <div className="view-switcher-group-title">
              JARVIS Communication Surface
            </div>
            <div
              className="view-switcher"
              style={{
                display: "flex",
                flexWrap: "nowrap",
                overflowX: "auto",
                gap: 8,
              }}
            >
              {jarvisChatSections.map((section) => (
                <button
                  key={section}
                  type="button"
                  className={
                    activeJarvisChatSection === section
                      ? "view-switch-button active"
                      : "view-switch-button"
                  }
                  onClick={() => onJarvisChatSectionChange(section)}
                >
                  {getJarvisChatSectionTitle(section)}
                </button>
              ))}
            </div>
          </section>
        ) : null}

        {showSurfaceSelector ? (
          <section
            className="view-switcher-group"
            style={{
              opacity: collapseSurfaceSelector ? 0.72 : 1,
            }}
          >
            <div className="view-switcher-group-title">
              Primary Surface Exposure
            </div>
            <div
              className="view-switcher"
              style={{
                display: "flex",
                flexWrap: "nowrap",
                overflowX: "auto",
                gap: 8,
              }}
            >
              {topDrawerExposureGroup?.rows.map((row) => (
                <button
                  key={row.surfaceId}
                  type="button"
                  className={
                    row.surfaceId === activeEmbeddedChatSurface
                      ? "view-switch-button active"
                      : "view-switch-button"
                  }
                  onClick={() => onEmbeddedChatSurfaceChange(row.surfaceId)}
                >
                  {row.title}
                </button>
              )) ?? null}
            </div>
          </section>
        ) : null}

        {showSummaryChipLane ? (
          <div
            style={{
              display: "flex",
              gap: 8,
              flexWrap: "nowrap",
              overflowX: "auto",
              paddingBottom: 2,
              opacity: collapseSummaryChipLane ? 0.72 : 1,
            }}
          >
            {topDrawerExposureGroup?.rows.map((row) => (
              <span
                key={row.surfaceId}
                className="inspect-chip"
                style={{ whiteSpace: "nowrap" }}
              >
                {row.title}: {row.countLabel} {row.countValue}
              </span>
            )) ?? null}
          </div>
        ) : null}

        {showSupportMeta ? (
          <div
            style={{
              display: "flex",
              gap: 8,
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <span className="inspect-chip">
              Density Mode: {topCommunicationDensityMode}
            </span>
            <span className="inspect-chip">
              Content Dominant: {String(contentDominant)}
            </span>
          </div>
        ) : null}

        <div
          style={{
            minHeight: 0,
            overflow: "auto",
            paddingRight: 4,
            borderTop: contentDominant
              ? "1px solid rgba(255,255,255,0.08)"
              : "none",
            paddingTop: contentDominant ? 10 : 0,
          }}
        >
          {renderTopDrawerBody()}
        </div>
      </div>
    </section>
  );
}
