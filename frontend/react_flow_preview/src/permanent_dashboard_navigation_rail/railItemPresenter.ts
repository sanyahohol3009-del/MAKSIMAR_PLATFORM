import type {
  LeftDrawerSkeletonNavigationBadge,
} from "../leftDrawerSkeletonNavigationExposure.js";
import type {
  PermanentDashboardNavigationRailShellItem,
} from "./types.js";

export function getPermanentDashboardNavigationRailBadgeLabel(
  badge: LeftDrawerSkeletonNavigationBadge,
): string {
  switch (badge) {
    case "implemented":
      return "Implemented";
    case "reserved":
      return "Reserved";
    case "approval_required":
      return "Approval";
    case "adapter_boundary":
      return "Adapter";
    case "memory":
      return "Memory";
    case "mobile":
      return "Mobile";
    case "three_d":
      return "3D";
    case "simulation":
      return "Simulation";
  }
}

export function getPermanentDashboardNavigationRailItemAriaLabel(
  item: PermanentDashboardNavigationRailShellItem,
): string {
  const selectedText = item.selected ? "selected" : "not selected";
  const approvalText = item.requiresApproval ? "approval required" : "no approval required";
  const adapterText = item.adapterBoundaryRequired
    ? "adapter boundary"
    : "direct read model route";

  return `${item.title}, ${selectedText}, ${approvalText}, ${adapterText}`;
}

export function getPermanentDashboardNavigationRailItemClassName(
  item: PermanentDashboardNavigationRailShellItem,
): string {
  return [
    "permanent-dashboard-navigation-rail__item",
    `permanent-dashboard-navigation-rail__item--${item.visualKind}`,
    item.selected ? "permanent-dashboard-navigation-rail__item--selected" : "",
    item.requiresApproval
      ? "permanent-dashboard-navigation-rail__item--approval-required"
      : "",
    item.adapterBoundaryRequired
      ? "permanent-dashboard-navigation-rail__item--adapter-boundary"
      : "",
  ]
    .filter(Boolean)
    .join(" ");
}

export function getPermanentDashboardNavigationRailItemShortLabel(
  item: PermanentDashboardNavigationRailShellItem,
): string {
  const words = item.title
    .split(/[\s/]+/u)
    .map((word) => word.trim())
    .filter(Boolean);

  if (words.length === 0) {
    return item.title.slice(0, 2).toUpperCase();
  }

  return words
    .slice(0, 2)
    .map((word) => word[0]?.toUpperCase() ?? "")
    .join("");
}
