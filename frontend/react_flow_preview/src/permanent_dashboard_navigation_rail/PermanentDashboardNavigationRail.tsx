import * as React from "react";

import {
  getPermanentDashboardNavigationRailBadgeLabel,
  getPermanentDashboardNavigationRailItemAriaLabel,
  getPermanentDashboardNavigationRailItemClassName,
  getPermanentDashboardNavigationRailItemShortLabel,
} from "./railItemPresenter.js";
import {
  getPermanentDashboardNavigationRailSectionClassName,
  getPermanentDashboardNavigationRailSectionCountLabel,
  getPermanentDashboardNavigationRailSectionHeadingId,
} from "./railSectionPresenter.js";
import {
  buildPermanentDashboardNavigationRailShellReadModel,
} from "./railReadModelAdapter.js";
import type {
  PermanentDashboardNavigationRailShellItem,
  PermanentDashboardNavigationRailShellProps,
  PermanentDashboardNavigationRailShellReadModel,
  PermanentDashboardNavigationRailShellSection,
} from "./types.js";

function buildRailStyle(
  readModel: PermanentDashboardNavigationRailShellReadModel,
): React.CSSProperties {
  return {
    width: readModel.density === "compact" ? 104 : 284,
    minWidth: readModel.density === "compact" ? 104 : 284,
    height: "100%",
    display: "flex",
    flexDirection: "column",
    gap: 10,
    padding: "14px 10px",
    boxSizing: "border-box",
    borderRight: "1px solid rgba(122, 220, 255, 0.18)",
    background:
      "linear-gradient(180deg, rgba(7, 14, 28, 0.94), rgba(3, 7, 16, 0.98))",
    boxShadow: "inset -1px 0 0 rgba(255, 255, 255, 0.04)",
    color: "rgba(235, 249, 255, 0.94)",
    overflow: "hidden",
  };
}

const sectionListStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 10,
  overflowY: "auto",
  overflowX: "hidden",
  paddingRight: 2,
};

const headerStyle: React.CSSProperties = {
  display: "grid",
  gap: 4,
  padding: "0 4px 8px",
  borderBottom: "1px solid rgba(122, 220, 255, 0.12)",
};

const eyebrowStyle: React.CSSProperties = {
  fontSize: 10,
  letterSpacing: "0.16em",
  textTransform: "uppercase",
  color: "rgba(122, 220, 255, 0.72)",
};

const titleStyle: React.CSSProperties = {
  margin: 0,
  fontSize: 13,
  lineHeight: 1.2,
  fontWeight: 700,
};

const sectionStyle: React.CSSProperties = {
  display: "grid",
  gap: 5,
};

const sectionHeaderStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: 8,
  padding: "0 4px",
};

const sectionTitleStyle: React.CSSProperties = {
  fontSize: 10,
  letterSpacing: "0.12em",
  textTransform: "uppercase",
  color: "rgba(189, 231, 255, 0.62)",
  whiteSpace: "nowrap",
  overflow: "hidden",
  textOverflow: "ellipsis",
};

const sectionCountStyle: React.CSSProperties = {
  fontSize: 10,
  color: "rgba(255, 183, 96, 0.78)",
};

const itemButtonStyle: React.CSSProperties = {
  width: "100%",
  display: "grid",
  gridTemplateColumns: "32px minmax(0, 1fr)",
  alignItems: "center",
  gap: 8,
  padding: "7px 8px",
  border: "1px solid rgba(122, 220, 255, 0.12)",
  borderRadius: 12,
  background: "rgba(12, 28, 50, 0.46)",
  color: "inherit",
  cursor: "pointer",
  textAlign: "left",
};

const selectedItemButtonStyle: React.CSSProperties = {
  borderColor: "rgba(122, 220, 255, 0.55)",
  background:
    "linear-gradient(135deg, rgba(33, 143, 196, 0.32), rgba(255, 157, 64, 0.12))",
  boxShadow: "0 0 18px rgba(44, 171, 224, 0.16)",
};

const iconStyle: React.CSSProperties = {
  width: 30,
  height: 30,
  borderRadius: 10,
  display: "grid",
  placeItems: "center",
  border: "1px solid rgba(122, 220, 255, 0.2)",
  background: "rgba(122, 220, 255, 0.08)",
  fontSize: 11,
  fontWeight: 800,
  color: "rgba(220, 247, 255, 0.92)",
};

const textStackStyle: React.CSSProperties = {
  minWidth: 0,
  display: "grid",
  gap: 3,
};

const itemTitleStyle: React.CSSProperties = {
  fontSize: 12,
  fontWeight: 650,
  whiteSpace: "nowrap",
  overflow: "hidden",
  textOverflow: "ellipsis",
};

const badgeRowStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: 3,
};

const badgeStyle: React.CSSProperties = {
  fontSize: 9,
  lineHeight: 1.1,
  padding: "2px 4px",
  borderRadius: 999,
  color: "rgba(222, 244, 255, 0.78)",
  background: "rgba(255, 255, 255, 0.06)",
  border: "1px solid rgba(255, 255, 255, 0.07)",
};

function renderBadges(item: PermanentDashboardNavigationRailShellItem): React.ReactNode {
  return (
    <span style={badgeRowStyle} aria-hidden="true">
      {item.badges.slice(0, 3).map((badge) => (
        <span key={`${item.surfaceId}:${badge}`} style={badgeStyle}>
          {getPermanentDashboardNavigationRailBadgeLabel(badge)}
        </span>
      ))}
    </span>
  );
}

function renderItem(
  item: PermanentDashboardNavigationRailShellItem,
  readModel: PermanentDashboardNavigationRailShellReadModel,
  onSelectSurface?: (surfaceId: string) => void,
): React.ReactNode {
  const handleClick = (): void => {
    if (!item.disabled && onSelectSurface) {
      onSelectSurface(item.surfaceId);
    }
  };

  return (
    <button
      key={item.railItemId}
      type="button"
      className={getPermanentDashboardNavigationRailItemClassName(item)}
      style={{
        ...itemButtonStyle,
        ...(item.selected ? selectedItemButtonStyle : {}),
      }}
      disabled={item.disabled}
      aria-current={item.selected ? "page" : undefined}
      aria-label={getPermanentDashboardNavigationRailItemAriaLabel(item)}
      data-surface-id={item.surfaceId}
      data-renderer-adapter-id={item.rendererAdapterId}
      data-visual-kind={item.visualKind}
      onClick={handleClick}
    >
      <span style={iconStyle}>
        {getPermanentDashboardNavigationRailItemShortLabel(item)}
      </span>

      {readModel.density === "expanded" ? (
        <span style={textStackStyle}>
          <span style={itemTitleStyle}>{item.title}</span>
          {renderBadges(item)}
        </span>
      ) : (
        <span style={textStackStyle}>
          <span style={itemTitleStyle}>{item.title}</span>
        </span>
      )}
    </button>
  );
}

function renderSection(
  section: PermanentDashboardNavigationRailShellSection,
  readModel: PermanentDashboardNavigationRailShellReadModel,
  onSelectSurface?: (surfaceId: string) => void,
): React.ReactNode {
  const headingId = getPermanentDashboardNavigationRailSectionHeadingId(section);

  return (
    <section
      key={section.buttonGroup}
      className={getPermanentDashboardNavigationRailSectionClassName(section)}
      style={sectionStyle}
      aria-labelledby={headingId}
    >
      <div style={sectionHeaderStyle}>
        <span id={headingId} style={sectionTitleStyle}>
          {section.title}
        </span>
        <span style={sectionCountStyle}>
          {getPermanentDashboardNavigationRailSectionCountLabel(section)}
        </span>
      </div>

      {section.items.map((item) => renderItem(item, readModel, onSelectSurface))}
    </section>
  );
}

export function PermanentDashboardNavigationRail(
  props: PermanentDashboardNavigationRailShellProps,
): React.ReactElement {
  const readModel =
    props.readModel ??
    buildPermanentDashboardNavigationRailShellReadModel({
      ...(props.activeSurfaceId !== undefined
        ? { activeSurfaceId: props.activeSurfaceId }
        : {}),
      ...(props.density !== undefined ? { density: props.density } : {}),
    });

  return (
    <nav
      className={props.className ?? "permanent-dashboard-navigation-rail"}
      style={buildRailStyle(readModel)}
      aria-label="Permanent dashboard navigation rail"
      data-target={readModel.target}
      data-placement={readModel.placement}
      data-density={readModel.density}
      data-active-surface-id={readModel.activeSurfaceId}
    >
      <header style={headerStyle}>
        <span style={eyebrowStyle}>MAKSIMAR</span>
        <h2 style={titleStyle}>Dashboard Rail</h2>
      </header>

      <div style={sectionListStyle}>
        {readModel.sections.map((section) =>
          renderSection(section, readModel, props.onSelectSurface),
        )}
      </div>
    </nav>
  );
}
