import type { ChartViewKey } from "./chartTelemetryRegistry.js";
import type { GraphViewKey } from "./graphProjectionTypes.js";
import {
  buildUnifiedVisualWorkspaceSnapshot,
} from "./unifiedVisualWorkspace.js";
import {
  getUnifiedVisualWorkspaceRegistryEntry,
  type UnifiedVisualViewId,
} from "./unifiedVisualWorkspaceRegistry.js";
import {
  extractChartViewKey,
  extractGraphViewKey,
  isChartViewId,
  isGraphViewId,
} from "./shell/activeVisualViewHelpers.js";

export type ActiveDashboardRouteKind = "graph" | "chart";

export type ActiveDashboardRouteReadModel = {
  activeView: UnifiedVisualViewId;
  activeKind: ActiveDashboardRouteKind;
  activeEntry: ReturnType<typeof getUnifiedVisualWorkspaceRegistryEntry>;
  workspaceSnapshot: ReturnType<typeof buildUnifiedVisualWorkspaceSnapshot>;
  activeGraphViewKey: GraphViewKey | null;
  activeChartViewKey: ChartViewKey | null;
};

export function buildActiveDashboardRouteReadModel(
  activeView: UnifiedVisualViewId,
): ActiveDashboardRouteReadModel {
  const activeEntry = getUnifiedVisualWorkspaceRegistryEntry(activeView);
  const workspaceSnapshot = buildUnifiedVisualWorkspaceSnapshot(activeView);

  const activeGraphViewKey = isGraphViewId(activeView)
    ? extractGraphViewKey(activeView)
    : null;

  const activeChartViewKey = isChartViewId(activeView)
    ? extractChartViewKey(activeView)
    : null;

  return {
    activeView,
    activeKind: activeGraphViewKey ? "graph" : "chart",
    activeEntry,
    workspaceSnapshot,
    activeGraphViewKey,
    activeChartViewKey,
  };
}
