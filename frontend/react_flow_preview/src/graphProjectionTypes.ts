export type GraphViewKey =
  | "topology"
  | "dependency"
  | "dataflow"
  | "modules"
  | "guard_chain"
  | "truth_consistency"
  | "workspace"
  | "displays";

export type ProjectionField = {
  key: string;
  value: string;
};

export type ProjectionNodeRecord = {
  id: string;
  title: string;
  subtitle: string;
  semanticKind: string;
  position: {
    x: number;
    y: number;
  };
  fields: ProjectionField[];
};

export type ProjectionEdgeRecord = {
  id: string;
  source: string;
  target: string;
  title: string;
  semanticKind: string;
  fields: ProjectionField[];
};

export type GraphProjectionView = {
  title: string;
  subtitle: string;
  inspectHint: string;
  nodes: ProjectionNodeRecord[];
  edges: ProjectionEdgeRecord[];
};

export type GraphProjectionRegistry = Record<GraphViewKey, GraphProjectionView>;
