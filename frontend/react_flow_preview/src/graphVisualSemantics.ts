import type { CSSProperties } from "react";
import type { Edge, Node } from "@xyflow/react";

import { graphProjectionRegistry } from "./graphProjectionData.js";
import type {
  GraphViewKey,
  ProjectionEdgeRecord,
  ProjectionNodeRecord,
} from "./graphProjectionTypes.js";

type StyledNodeData = {
  label: string;
};

function resolveNodeStyle(node: ProjectionNodeRecord): CSSProperties {
  switch (node.semanticKind) {
    case "topology_anchor_node":
      return {
        border: "1px solid #4f7cff",
        background: "#1d2a4a",
        color: "#ffffff",
        minWidth: "220px",
      };
    case "topology_execution_node":
      return {
        border: "1px solid #2f8f6b",
        background: "#173229",
        color: "#ffffff",
        minWidth: "220px",
      };
    case "module_surface":
      return {
        border: "1px solid #a56eff",
        background: "#2a1e47",
        color: "#ffffff",
        minWidth: "240px",
      };
    case "dependency_node":
      return {
        border: "1px solid #ffb347",
        background: "#3a2814",
        color: "#ffffff",
        minWidth: "210px",
      };
    case "dataflow_node":
      return {
        border: "1px solid #54c7ec",
        background: "#173544",
        color: "#ffffff",
        minWidth: "210px",
      };
    case "guard_chain_node":
      return {
        border: "1px solid #ff6b6b",
        background: "#3b1f24",
        color: "#ffffff",
        minWidth: "220px",
      };
    case "truth_consistency_node":
      return {
        border: "1px solid #ffd166",
        background: "#3b3018",
        color: "#ffffff",
        minWidth: "240px",
      };
    case "workspace_display_node":
      return {
        border: "1px solid #6ee7ff",
        background: "#173544",
        color: "#ffffff",
        minWidth: "220px",
      };
    case "workspace_panel_node":
      return {
        border: "1px solid #9ca3af",
        background: "#222a36",
        color: "#ffffff",
        minWidth: "220px",
      };
    case "display_target_node":
      return {
        border: "1px solid #5b8cff",
        background: "#1d2a4a",
        color: "#ffffff",
        minWidth: "240px",
      };
    case "display_surface_node":
      return {
        border: "1px solid #c58cff",
        background: "#2a1e47",
        color: "#ffffff",
        minWidth: "250px",
      };
    default:
      return {
        border: "1px solid #344056",
        background: "#1b2333",
        color: "#ffffff",
        minWidth: "200px",
      };
  }
}

function resolveEdgeStyle(edge: ProjectionEdgeRecord): {
  stroke: string;
  strokeWidth: number;
  animated: boolean;
} {
  switch (edge.semanticKind) {
    case "topology_anchor_edge":
      return {
        stroke: "#7aa2ff",
        strokeWidth: 2,
        animated: false,
      };
    case "execution_dependency":
      return {
        stroke: "#ffb347",
        strokeWidth: 2,
        animated: false,
      };
    case "projection_dependency":
      return {
        stroke: "#c58cff",
        strokeWidth: 2,
        animated: false,
      };
    case "control_to_execution":
    case "execution_to_workers":
    case "workers_to_data_plane":
    case "observability_projection":
    case "control_to_observability":
      return {
        stroke: "#58d1f8",
        strokeWidth: 2.4,
        animated: true,
      };
    case "surface_navigation_continuity":
    case "audit_visibility_relation":
      return {
        stroke: "#b57cff",
        strokeWidth: 2,
        animated: false,
      };
    case "guard_chain_relation":
      return {
        stroke: "#ff7b7b",
        strokeWidth: 2.4,
        animated: true,
      };
    case "truth_consistency_relation":
      return {
        stroke: "#ffd166",
        strokeWidth: 2.2,
        animated: false,
      };
    case "workspace_placement_relation":
      return {
        stroke: "#6ee7ff",
        strokeWidth: 2,
        animated: false,
      };
    case "display_assignment_relation":
      return {
        stroke: "#c58cff",
        strokeWidth: 2.2,
        animated: true,
      };
    default:
      return {
        stroke: "#8ea3c8",
        strokeWidth: 1.8,
        animated: false,
      };
  }
}

export function buildStyledNodes(viewKey: GraphViewKey): Node<StyledNodeData>[] {
  return graphProjectionRegistry[viewKey].nodes.map((node) => ({
    id: node.id,
    position: node.position,
    data: {
      label: `${node.title}\n${node.subtitle}`,
    },
    type: "default",
    style: resolveNodeStyle(node),
  }));
}

export function buildStyledEdges(viewKey: GraphViewKey): Edge[] {
  return graphProjectionRegistry[viewKey].edges.map((edge) => {
    const styleConfig = resolveEdgeStyle(edge);

    return {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.title,
      animated: styleConfig.animated,
      style: {
        stroke: styleConfig.stroke,
        strokeWidth: styleConfig.strokeWidth,
      },
      labelStyle: {
        fill: "#dce6f5",
        fontSize: 11,
      },
    };
  });
}
