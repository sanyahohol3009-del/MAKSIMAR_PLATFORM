import { graphProjectionRegistry } from "./graphProjectionData.js";
import type {
  GraphViewKey,
  ProjectionEdgeRecord,
  ProjectionField,
  ProjectionNodeRecord,
} from "./graphProjectionTypes.js";

export type InspectSection = {
  title: string;
  items: ProjectionField[];
};

export type InspectPresentation = {
  title: string;
  subtitle: string;
  semanticKind: string;
  explanation: string;
  sections: InspectSection[];
};

function toReadableLabel(key: string): string {
  return key
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function groupFields(fields: ProjectionField[]): InspectSection[] {
  const primary: ProjectionField[] = [];
  const routing: ProjectionField[] = [];
  const projection: ProjectionField[] = [];
  const flags: ProjectionField[] = [];
  const other: ProjectionField[] = [];

  for (const field of fields) {
    if (
      field.key.includes("role") ||
      field.key.includes("kind") ||
      field.key.includes("surface") ||
      field.key.includes("domain") ||
      field.key.includes("workspace")
    ) {
      primary.push({ key: toReadableLabel(field.key), value: field.value });
      continue;
    }

    if (
      field.key.includes("source") ||
      field.key.includes("target") ||
      field.key.includes("upstream") ||
      field.key.includes("downstream") ||
      field.key.includes("from") ||
      field.key.includes("to")
    ) {
      routing.push({ key: toReadableLabel(field.key), value: field.value });
      continue;
    }

    if (
      field.key.includes("projection") ||
      field.key.includes("surface_id") ||
      field.key.includes("navigation_id") ||
      field.key.includes("registry_audit_id")
    ) {
      projection.push({ key: toReadableLabel(field.key), value: field.value });
      continue;
    }

    if (
      field.key.includes("visible") ||
      field.key.includes("allowed") ||
      field.key.includes("root")
    ) {
      flags.push({ key: toReadableLabel(field.key), value: field.value });
      continue;
    }

    other.push({ key: toReadableLabel(field.key), value: field.value });
  }

  const sections: InspectSection[] = [];

  if (primary.length > 0) {
    sections.push({ title: "Primary Semantics", items: primary });
  }
  if (routing.length > 0) {
    sections.push({ title: "Routing / Relations", items: routing });
  }
  if (projection.length > 0) {
    sections.push({ title: "Projection Bindings", items: projection });
  }
  if (flags.length > 0) {
    sections.push({ title: "Flags / Visibility", items: flags });
  }
  if (other.length > 0) {
    sections.push({ title: "Additional Details", items: other });
  }

  return sections;
}

function buildNodeExplanation(
  viewKey: GraphViewKey,
  node: ProjectionNodeRecord,
): string {
  switch (viewKey) {
    case "topology":
      return `${node.title} is a topology node in the ${node.subtitle} role. This view explains where the node sits in the topology graph and which canonical capabilities are attached to it.`;

    case "dependency":
      return `${node.title} is a dependency graph node. This view explains how the module participates in upstream/downstream contract relationships.`;

    case "dataflow":
      return `${node.title} is a dataflow node. This view explains how requests, execution, telemetry, or artifacts move through the system.`;

    case "modules":
      return `${node.title} is a module graph node. This view explains module role, workspace, surface bindings, and audit/navigation continuity.`;

    case "guard_chain":
      return `${node.title} is part of the safety guard chain. This view explains ordered protection layers and their canonical placement in the runtime safety sequence.`;

    case "truth_consistency":
      return `${node.title} is a truth-consistency node. This view explains which panel and truth scope are bound together in the read-only consistency layer.`;

    case "workspace":
      return `${node.title} is part of the workspace graph. This view explains how displays, panels, zones, and slot placements are arranged in the operator workspace model.`;

    case "displays":
      return `${node.title} is part of the display-assignment graph. This view explains how surfaces are assigned to display targets and whether those assignments are replaceable or fixed.`;
  }
}

function buildEdgeExplanation(
  viewKey: GraphViewKey,
  edge: ProjectionEdgeRecord,
): string {
  switch (viewKey) {
    case "topology":
      return `${edge.title} is a topology relation. This edge explains anchor structure between canonical topology nodes.`;

    case "dependency":
      return `${edge.title} is a dependency relation. This edge explains why one module is upstream or downstream of another.`;

    case "dataflow":
      return `${edge.title} is a dataflow relation. This edge explains how requests, execution, artifacts, or telemetry move from source to target.`;

    case "modules":
      return `${edge.title} is a module-level relation. This edge explains surface continuity, navigation continuity, or audit visibility between modules.`;

    case "guard_chain":
      return `${edge.title} is a guard-chain relation. This edge explains the canonical order of safety enforcement layers in the runtime protection chain.`;

    case "truth_consistency":
      return `${edge.title} is a truth-consistency relation. This edge explains how truth scopes are sequenced and correlated in the read-only consistency view.`;

    case "workspace":
      return `${edge.title} is a workspace placement relation. This edge explains how a panel placement is bound to a display target inside the workspace model.`;

    case "displays":
      return `${edge.title} is a display-assignment relation. This edge explains which surface is assigned to which display target and under what assignment state.`;
  }
}

export function buildNodeInspectPresentation(
  viewKey: GraphViewKey,
  node: ProjectionNodeRecord,
): InspectPresentation {
  return {
    title: node.title,
    subtitle: node.subtitle,
    semanticKind: node.semanticKind,
    explanation: buildNodeExplanation(viewKey, node),
    sections: groupFields(node.fields),
  };
}

export function buildEdgeInspectPresentation(
  viewKey: GraphViewKey,
  edge: ProjectionEdgeRecord,
): InspectPresentation {
  return {
    title: edge.title,
    subtitle: `${edge.source} → ${edge.target}`,
    semanticKind: edge.semanticKind,
    explanation: buildEdgeExplanation(viewKey, edge),
    sections: groupFields(edge.fields),
  };
}

export function buildDefaultInspectPresentation(
  viewKey: GraphViewKey,
): InspectPresentation {
  const view = graphProjectionRegistry[viewKey];

  return {
    title: view.title,
    subtitle: view.subtitle,
    semanticKind: "view_overview",
    explanation: view.inspectHint,
    sections: [
      {
        title: "View Summary",
        items: [
          { key: "Nodes", value: String(view.nodes.length) },
          { key: "Edges", value: String(view.edges.length) },
        ],
      },
    ],
  };
}
