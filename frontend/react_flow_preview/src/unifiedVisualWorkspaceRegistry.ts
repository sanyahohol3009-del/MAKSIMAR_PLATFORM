import {
  canonicalGraphRegistry,
} from "./canonicalGraphRegistry.js";
import {
  chartTelemetryRegistry,
} from "./chartTelemetryRegistry.js";
import type { ChartViewKey } from "./chartTelemetryRegistry.js";
import type { GraphViewKey } from "./graphProjectionTypes.js";

export type UnifiedVisualViewKind = "graph" | "chart";

export type UnifiedVisualViewId =
  | `graph:${GraphViewKey}`
  | `chart:${ChartViewKey}`;

export type UnifiedVisualRegistryGroup =
  | "execution_graphs"
  | "operator_graphs"
  | "foundation_graphs"
  | "display_graphs"
  | "telemetry_charts";

export type UnifiedVisualWorkspaceRegistryEntry = {
  viewId: UnifiedVisualViewId;
  viewKind: UnifiedVisualViewKind;
  rawViewKey: GraphViewKey | ChartViewKey;
  group: UnifiedVisualRegistryGroup;
  order: number;
  title: string;
  subtitle: string;
  inspectHint: string;
  summaryLabel: string;
  summaryValue: number;
};

const graphEntries: UnifiedVisualWorkspaceRegistryEntry[] =
  canonicalGraphRegistry.map((entry) => ({
    viewId: `graph:${entry.viewKey}` as const,
    viewKind: "graph",
    rawViewKey: entry.viewKey,
    group: entry.group,
    order: entry.order,
    title: entry.title,
    subtitle: entry.subtitle,
    inspectHint: entry.inspectHint,
    summaryLabel: "Nodes",
    summaryValue: entry.nodeCount,
  }));

const chartEntries: UnifiedVisualWorkspaceRegistryEntry[] =
  chartTelemetryRegistry.map((entry, index) => ({
    viewId: `chart:${entry.viewKey}` as const,
    viewKind: "chart",
    rawViewKey: entry.viewKey,
    group: "telemetry_charts",
    order: canonicalGraphRegistry.length + index + 1,
    title: entry.title,
    subtitle: entry.subtitle,
    inspectHint: `Inspect ${entry.chartKind} telemetry semantics and visible series points.`,
    summaryLabel: "Series Points",
    summaryValue: entry.series.length,
  }));

export const unifiedVisualWorkspaceRegistry:
  ReadonlyArray<UnifiedVisualWorkspaceRegistryEntry> = [
    ...graphEntries,
    ...chartEntries,
  ].sort((left, right) => left.order - right.order);

export function getUnifiedVisualWorkspaceRegistryEntry(
  viewId: UnifiedVisualViewId,
): UnifiedVisualWorkspaceRegistryEntry {
  const entry = unifiedVisualWorkspaceRegistry.find(
    (registryEntry) => registryEntry.viewId === viewId,
  );
  if (!entry) {
    throw new Error(`Missing unified visual registry entry for ${viewId}.`);
  }
  return entry;
}

export function getUnifiedVisualViewOrder(): UnifiedVisualViewId[] {
  return unifiedVisualWorkspaceRegistry.map((entry) => entry.viewId);
}

export function getUnifiedVisualRegistryGroups(): ReadonlyArray<{
  group: UnifiedVisualRegistryGroup;
  title: string;
  viewIds: UnifiedVisualViewId[];
}> {
  const groupTitles: Record<UnifiedVisualRegistryGroup, string> = {
    execution_graphs: "Execution Graphs",
    operator_graphs: "Operator Graphs",
    foundation_graphs: "Foundation Graphs",
    display_graphs: "Display Graphs",
    telemetry_charts: "Telemetry Charts",
  };

  const groupOrder: readonly UnifiedVisualRegistryGroup[] = [
    "execution_graphs",
    "operator_graphs",
    "foundation_graphs",
    "display_graphs",
    "telemetry_charts",
  ];

  const grouped = new Map<UnifiedVisualRegistryGroup, UnifiedVisualViewId[]>();

  for (const entry of unifiedVisualWorkspaceRegistry) {
    const existing = grouped.get(entry.group) ?? [];
    existing.push(entry.viewId);
    grouped.set(entry.group, existing);
  }

  return groupOrder.map((group) => ({
    group,
    title: groupTitles[group],
    viewIds: grouped.get(group) ?? [],
  }));
}
