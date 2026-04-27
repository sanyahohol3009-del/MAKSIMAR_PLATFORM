import type {
  PermanentDashboardNavigationRailShellSection,
} from "./types.js";

export function getPermanentDashboardNavigationRailSectionHeadingId(
  section: PermanentDashboardNavigationRailShellSection,
): string {
  return `permanent-dashboard-navigation-rail-section-${section.buttonGroup}`;
}

export function getPermanentDashboardNavigationRailSectionClassName(
  section: PermanentDashboardNavigationRailShellSection,
): string {
  return [
    "permanent-dashboard-navigation-rail__section",
    `permanent-dashboard-navigation-rail__section--${section.buttonGroup}`,
  ].join(" ");
}

export function getPermanentDashboardNavigationRailSectionCountLabel(
  section: PermanentDashboardNavigationRailShellSection,
): string {
  return `${section.items.length}`;
}
