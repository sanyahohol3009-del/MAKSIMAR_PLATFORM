import {
  getUnifiedVisualRegistryGroups,
  getUnifiedVisualViewOrder,
  getUnifiedVisualWorkspaceRegistryEntry,
  unifiedVisualWorkspaceRegistry,
} from "./unifiedVisualWorkspaceRegistry.js";
import type {
  UnifiedVisualViewId,
  UnifiedVisualViewKind,
} from "./unifiedVisualWorkspaceRegistry.js";

export type UnifiedVisualWorkspaceViewSummary = {
  viewId: UnifiedVisualViewId;
  viewKind: UnifiedVisualViewKind;
  rawViewKey: string;
  group: string;
  order: number;
  title: string;
  subtitle: string;
  inspectHint: string;
  summaryLabel: string;
  summaryValue: number;
};

export type UnifiedVisualWorkspaceSnapshot = {
  totalViews: number;
  totalGraphViews: number;
  totalChartViews: number;
  activeView: UnifiedVisualWorkspaceViewSummary;
  groupedViews: ReadonlyArray<{
    group: string;
    title: string;
    views: UnifiedVisualWorkspaceViewSummary[];
  }>;
};

export function getNextUnifiedVisualViewId(
  current: UnifiedVisualViewId,
): UnifiedVisualViewId {
  const ordered = getUnifiedVisualViewOrder();
  const index = ordered.indexOf(current);

  if (index < 0) {
    throw new Error(`Unknown unified visual view id: ${current}`);
  }

  return ordered[(index + 1) % ordered.length]!;
}

export function getPreviousUnifiedVisualViewId(
  current: UnifiedVisualViewId,
): UnifiedVisualViewId {
  const ordered = getUnifiedVisualViewOrder();
  const index = ordered.indexOf(current);

  if (index < 0) {
    throw new Error(`Unknown unified visual view id: ${current}`);
  }

  return ordered[(index - 1 + ordered.length) % ordered.length]!;
}

export function buildUnifiedVisualWorkspaceSnapshot(
  activeViewId: UnifiedVisualViewId,
): UnifiedVisualWorkspaceSnapshot {
  const activeEntry = getUnifiedVisualWorkspaceRegistryEntry(activeViewId);

  const groupedViews = getUnifiedVisualRegistryGroups().map((group) => ({
    group: group.group,
    title: group.title,
    views: group.viewIds.map((viewId) => {
      const entry = getUnifiedVisualWorkspaceRegistryEntry(viewId);
      return {
        viewId: entry.viewId,
        viewKind: entry.viewKind,
        rawViewKey: entry.rawViewKey,
        group: entry.group,
        order: entry.order,
        title: entry.title,
        subtitle: entry.subtitle,
        inspectHint: entry.inspectHint,
        summaryLabel: entry.summaryLabel,
        summaryValue: entry.summaryValue,
      };
    }),
  }));

  return {
    totalViews: unifiedVisualWorkspaceRegistry.length,
    totalGraphViews: unifiedVisualWorkspaceRegistry.filter(
      (entry) => entry.viewKind === "graph",
    ).length,
    totalChartViews: unifiedVisualWorkspaceRegistry.filter(
      (entry) => entry.viewKind === "chart",
    ).length,
    activeView: {
      viewId: activeEntry.viewId,
      viewKind: activeEntry.viewKind,
      rawViewKey: activeEntry.rawViewKey,
      group: activeEntry.group,
      order: activeEntry.order,
      title: activeEntry.title,
      subtitle: activeEntry.subtitle,
      inspectHint: activeEntry.inspectHint,
      summaryLabel: activeEntry.summaryLabel,
      summaryValue: activeEntry.summaryValue,
    },
    groupedViews,
  };
}
