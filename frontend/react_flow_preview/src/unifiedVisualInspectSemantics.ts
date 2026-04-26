import {
  buildDefaultInspectPresentation,
  buildEdgeInspectPresentation,
  buildNodeInspectPresentation,
} from "./graphInspectSemantics.js";
import {
  getChartRegistryEntry,
  type ChartViewKey,
} from "./chartTelemetryRegistry.js";
import type {
  GraphViewKey,
  ProjectionEdgeRecord,
  ProjectionNodeRecord,
} from "./graphProjectionTypes.js";
import type { UnifiedVisualViewId } from "./unifiedVisualWorkspaceRegistry.js";

export type UnifiedInspectPresentation =
  ReturnType<typeof buildDefaultInspectPresentation>;

export type SelectedGraphInspectItem =
  | {
      kind: "node";
      viewKey: GraphViewKey;
      payload: ProjectionNodeRecord;
    }
  | {
      kind: "edge";
      viewKey: GraphViewKey;
      payload: ProjectionEdgeRecord;
    };

function isGraphViewId(
  viewId: UnifiedVisualViewId,
): viewId is `graph:${GraphViewKey}` {
  return viewId.startsWith("graph:");
}

function extractGraphViewKey(viewId: `graph:${GraphViewKey}`): GraphViewKey {
  return viewId.slice("graph:".length) as GraphViewKey;
}

function extractChartViewKey(viewId: `chart:${ChartViewKey}`): ChartViewKey {
  return viewId.slice("chart:".length) as ChartViewKey;
}

export function buildUnifiedVisualInspectPresentation(
  viewId: UnifiedVisualViewId,
  selectedItem: SelectedGraphInspectItem | null,
): UnifiedInspectPresentation {
  if (isGraphViewId(viewId)) {
    const graphViewKey = extractGraphViewKey(viewId);

    if (!selectedItem) {
      return buildDefaultInspectPresentation(graphViewKey);
    }

    if (selectedItem.kind === "node") {
      return buildNodeInspectPresentation(
        selectedItem.viewKey,
        selectedItem.payload,
      );
    }

    return buildEdgeInspectPresentation(
      selectedItem.viewKey,
      selectedItem.payload,
    );
  }

  const chartViewKey = extractChartViewKey(viewId as `chart:${ChartViewKey}`);
  const entry = getChartRegistryEntry(chartViewKey);

  return {
    title: entry.title,
    subtitle: entry.subtitle,
    semanticKind: `${entry.chartKind}_telemetry_chart`,
    explanation:
      "This chart view is part of the unified visual shell and reuses the shared inspect surface rather than opening a separate chart-only world.",
    sections: [
      {
        title: "Series Points",
        items: entry.series.map((point) => ({
          key: point.label,
          value: String(point.value),
        })),
      },
    ],
  };
}
