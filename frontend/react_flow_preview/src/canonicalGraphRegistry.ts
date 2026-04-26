import { graphProjectionRegistry } from "./graphProjectionData.js";
import type { GraphViewKey } from "./graphProjectionTypes.js";

export type CanonicalGraphRegistryGroup =
  | "execution_graphs"
  | "operator_graphs"
  | "foundation_graphs"
  | "display_graphs";

export type CanonicalGraphRegistryEntry = {
  viewKey: GraphViewKey;
  group: CanonicalGraphRegistryGroup;
  order: number;
  title: string;
  subtitle: string;
  inspectHint: string;
  nodeCount: number;
  edgeCount: number;
};

const registrySeed: ReadonlyArray<{
  viewKey: GraphViewKey;
  group: CanonicalGraphRegistryGroup;
  order: number;
}> = [
  { viewKey: "topology", group: "execution_graphs", order: 1 },
  { viewKey: "dependency", group: "execution_graphs", order: 2 },
  { viewKey: "dataflow", group: "execution_graphs", order: 3 },
  { viewKey: "modules", group: "operator_graphs", order: 4 },
  { viewKey: "guard_chain", group: "foundation_graphs", order: 5 },
  { viewKey: "truth_consistency", group: "foundation_graphs", order: 6 },
  { viewKey: "workspace", group: "display_graphs", order: 7 },
  { viewKey: "displays", group: "display_graphs", order: 8 },
];

export const canonicalGraphRegistry: ReadonlyArray<CanonicalGraphRegistryEntry> =
  registrySeed.map((seedEntry) => {
    const projection = graphProjectionRegistry[seedEntry.viewKey];

    return {
      viewKey: seedEntry.viewKey,
      group: seedEntry.group,
      order: seedEntry.order,
      title: projection.title,
      subtitle: projection.subtitle,
      inspectHint: projection.inspectHint,
      nodeCount: projection.nodes.length,
      edgeCount: projection.edges.length,
    };
  });

export function getCanonicalGraphViewOrder(): GraphViewKey[] {
  return canonicalGraphRegistry
    .slice()
    .sort((left, right) => left.order - right.order)
    .map((entry) => entry.viewKey);
}

export function getCanonicalGraphRegistryEntry(
  viewKey: GraphViewKey,
): CanonicalGraphRegistryEntry {
  const entry = canonicalGraphRegistry.find(
    (registryEntry) => registryEntry.viewKey === viewKey,
  );

  if (!entry) {
    throw new Error(`Missing canonical graph registry entry for ${viewKey}.`);
  }

  return entry;
}

export function getCanonicalGraphRegistryGroups(): ReadonlyArray<{
  group: CanonicalGraphRegistryGroup;
  title: string;
  viewKeys: GraphViewKey[];
}> {
  const ordered = canonicalGraphRegistry.slice().sort((a, b) => a.order - b.order);

  const groupTitles: Record<CanonicalGraphRegistryGroup, string> = {
    execution_graphs: "Execution Graphs",
    operator_graphs: "Operator Graphs",
    foundation_graphs: "Foundation Graphs",
    display_graphs: "Display Graphs",
  };

  const groupOrder: readonly CanonicalGraphRegistryGroup[] = [
    "execution_graphs",
    "operator_graphs",
    "foundation_graphs",
    "display_graphs",
  ];

  const grouped = new Map<CanonicalGraphRegistryGroup, GraphViewKey[]>();

  for (const entry of ordered) {
    const existing = grouped.get(entry.group) ?? [];
    existing.push(entry.viewKey);
    grouped.set(entry.group, existing);
  }

  return groupOrder.map((group) => ({
    group,
    title: groupTitles[group],
    viewKeys: grouped.get(group) ?? [],
  }));
}
