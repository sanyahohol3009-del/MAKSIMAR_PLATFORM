import test from "node:test";
import assert from "node:assert/strict";

import { graphProjectionRegistry } from "../react_flow_preview/src/graphProjectionData.js";
import {
  buildDefaultInspectPresentation,
  buildEdgeInspectPresentation,
  buildNodeInspectPresentation,
} from "../react_flow_preview/src/graphInspectSemantics.js";

test("default inspect presentation exposes view summary", () => {
  const inspect = buildDefaultInspectPresentation("topology");

  assert.equal(inspect.title, "Topology Graph");
  assert.equal(inspect.semanticKind, "view_overview");
  assert.equal(inspect.sections.length > 0, true);
});

test("node inspect presentation exposes grouped sections", () => {
  const node = graphProjectionRegistry.modules.nodes[0];

  if (!node) {
    throw new Error("Expected modules.nodes[0] to exist.");
  }

  const inspect = buildNodeInspectPresentation("modules", node);

  assert.equal(inspect.title, "module_manifest_001");
  assert.equal(inspect.semanticKind, "module_surface");
  assert.equal(inspect.sections.length > 0, true);
});

test("edge inspect presentation exposes readable subtitle", () => {
  const edge = graphProjectionRegistry.dataflow.edges[0];

  if (!edge) {
    throw new Error("Expected dataflow.edges[0] to exist.");
  }

  const inspect = buildEdgeInspectPresentation("dataflow", edge);

  assert.equal(inspect.title, "control request");
  assert.equal(inspect.subtitle, "control_plane → execution_control");
  assert.equal(inspect.sections.length > 0, true);
});
