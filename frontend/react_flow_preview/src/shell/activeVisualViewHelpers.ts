import type { ChartViewKey } from "../chartTelemetryRegistry.js";
import type { GraphViewKey } from "../graphProjectionTypes.js";
import type { UnifiedVisualViewId } from "../unifiedVisualWorkspaceRegistry.js";

export function isGraphViewId(
  viewId: UnifiedVisualViewId,
): viewId is `graph:${GraphViewKey}` {
  return viewId.startsWith("graph:");
}

export function isChartViewId(
  viewId: UnifiedVisualViewId,
): viewId is `chart:${ChartViewKey}` {
  return viewId.startsWith("chart:");
}

export function extractGraphViewKey(
  viewId: `graph:${GraphViewKey}`,
): GraphViewKey {
  return viewId.slice("graph:".length) as GraphViewKey;
}

export function extractChartViewKey(
  viewId: `chart:${ChartViewKey}`,
): ChartViewKey {
  return viewId.slice("chart:".length) as ChartViewKey;
}
