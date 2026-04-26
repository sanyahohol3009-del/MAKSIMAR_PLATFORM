import {
  canonicalGraphRegistry,
  getCanonicalGraphRegistryEntry,
  getCanonicalGraphRegistryGroups,
  getCanonicalGraphViewOrder,
} from "./canonicalGraphRegistry.js";
import type { GraphViewKey } from "./graphProjectionTypes.js";

export type UnifiedWorkspaceViewSummary = {
  viewKey: GraphViewKey;
  title: string;
  group: string;
  order: number;
  nodeCount: number;
  edgeCount: number;
  inspectHint: string;
};

export type UnifiedWorkspaceSnapshot = {
  totalViews: number;
  totalNodes: number;
  totalEdges: number;
  activeView: UnifiedWorkspaceViewSummary;
  groupedViews: ReadonlyArray<{
    group: string;
    title: string;
    views: UnifiedWorkspaceViewSummary[];
  }>;
};

export function getNextGraphViewKey(current: GraphViewKey): GraphViewKey {
  const ordered = getCanonicalGraphViewOrder();
  const index = ordered.indexOf(current);

  if (index < 0) {
    throw new Error(`Unknown graph view key: ${current}`);
  }

  return ordered[(index + 1) % ordered.length]!;
}

export function getPreviousGraphViewKey(current: GraphViewKey): GraphViewKey {
  const ordered = getCanonicalGraphViewOrder();
  const index = ordered.indexOf(current);

  if (index < 0) {
    throw new Error(`Unknown graph view key: ${current}`);
  }

  return ordered[(index - 1 + ordered.length) % ordered.length]!;
}

export function buildUnifiedWorkspaceSnapshot(
  activeViewKey: GraphViewKey,
): UnifiedWorkspaceSnapshot {
  const activeEntry = getCanonicalGraphRegistryEntry(activeViewKey);

  const groupedViews = getCanonicalGraphRegistryGroups().map((group) => ({
    group: group.group,
    title: group.title,
    views: group.viewKeys.map((viewKey) => {
      const entry = getCanonicalGraphRegistryEntry(viewKey);

      return {
        viewKey: entry.viewKey,
        title: entry.title,
        group: entry.group,
        order: entry.order,
        nodeCount: entry.nodeCount,
        edgeCount: entry.edgeCount,
        inspectHint: entry.inspectHint,
      };
    }),
  }));

  const totalNodes = canonicalGraphRegistry.reduce(
    (sum, entry) => sum + entry.nodeCount,
    0,
  );

  const totalEdges = canonicalGraphRegistry.reduce(
    (sum, entry) => sum + entry.edgeCount,
    0,
  );

  return {
    totalViews: canonicalGraphRegistry.length,
    totalNodes,
    totalEdges,
    activeView: {
      viewKey: activeEntry.viewKey,
      title: activeEntry.title,
      group: activeEntry.group,
      order: activeEntry.order,
      nodeCount: activeEntry.nodeCount,
      edgeCount: activeEntry.edgeCount,
      inspectHint: activeEntry.inspectHint,
    },
    groupedViews,
  };
}
