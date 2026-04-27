import React from "react";
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";

import type {
  GraphViewKey,
  ProjectionEdgeRecord,
  ProjectionNodeRecord,
} from "../graphProjectionTypes.js";

type CenterDashboardViewportProps = {
  activeGraphViewKey: GraphViewKey | null;
  nodes: Node[];
  edges: Edge[];
  chartHostRef: React.MutableRefObject<HTMLDivElement | null>;
  selectedNodeMap: Map<string, ProjectionNodeRecord>;
  selectedEdgeMap: Map<string, ProjectionEdgeRecord>;
  onNodeInspect: (args: {
    viewKey: GraphViewKey;
    payload: ProjectionNodeRecord;
  }) => void;
  onEdgeInspect: (args: {
    viewKey: GraphViewKey;
    payload: ProjectionEdgeRecord;
  }) => void;
};

export function CenterDashboardViewport({
  activeGraphViewKey,
  nodes,
  edges,
  chartHostRef,
  selectedNodeMap,
  selectedEdgeMap,
  onNodeInspect,
  onEdgeInspect,
}: CenterDashboardViewportProps) {
  return (
    <section
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 1,
      }}
    >
      {activeGraphViewKey ? (
        <div style={{ position: "absolute", inset: 0 }}>
          <ReactFlow
            key={`graph-flow:${activeGraphViewKey}`}
            nodes={nodes}
            edges={edges}
            fitView
            attributionPosition="bottom-left"
            proOptions={{ hideAttribution: true }}
            nodesDraggable={false}
            nodesConnectable={false}
            elementsSelectable={true}
            panOnDrag={true}
            zoomOnScroll={true}
            zoomOnPinch={true}
            onInit={(instance) => {
              window.requestAnimationFrame(() => {
                instance.fitView({ padding: 0.16 });
              });
            }}
            onNodeClick={(_, node) => {
              const payload = selectedNodeMap.get(node.id);
              if (payload) {
                onNodeInspect({
                  viewKey: activeGraphViewKey,
                  payload,
                });
              }
            }}
            onEdgeClick={(_, edge) => {
              const payload = selectedEdgeMap.get(edge.id);
              if (payload) {
                onEdgeInspect({
                  viewKey: activeGraphViewKey,
                  payload,
                });
              }
            }}
          >
            <MiniMap />
            <Controls />
            <Background />
          </ReactFlow>
        </div>
      ) : (
        <div
          style={{
            position: "absolute",
            inset: 0,
            paddingTop: 58,
          }}
        >
          <div ref={chartHostRef} className="chart-host" />
        </div>
      )}
    </section>
  );
}
