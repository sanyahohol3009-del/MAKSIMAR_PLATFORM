import test from "node:test";
import assert from "node:assert/strict";

import { graphProjectionRegistry } from "../react_flow_preview/src/graphProjectionData.js";

test("graph projection registry contains all canonical graph views", () => {
  assert.deepEqual(Object.keys(graphProjectionRegistry), [
    "topology",
    "dependency",
    "dataflow",
    "modules",
    "guard_chain",
    "truth_consistency",
    "workspace",
    "displays",
  ]);
});

test("graph projection registry node/edge totals remain stable", () => {
  assert.equal(graphProjectionRegistry.topology.nodes.length, 3);
  assert.equal(graphProjectionRegistry.topology.edges.length, 2);

  assert.equal(graphProjectionRegistry.dependency.nodes.length, 4);
  assert.equal(graphProjectionRegistry.dependency.edges.length, 3);

  assert.equal(graphProjectionRegistry.dataflow.nodes.length, 6);
  assert.equal(graphProjectionRegistry.dataflow.edges.length, 5);

  assert.equal(graphProjectionRegistry.modules.nodes.length, 3);
  assert.equal(graphProjectionRegistry.modules.edges.length, 3);

  assert.equal(graphProjectionRegistry.guard_chain.nodes.length, 4);
  assert.equal(graphProjectionRegistry.guard_chain.edges.length, 3);

  assert.equal(graphProjectionRegistry.truth_consistency.nodes.length, 4);
  assert.equal(graphProjectionRegistry.truth_consistency.edges.length, 3);

  assert.equal(graphProjectionRegistry.workspace.nodes.length, 10);
  assert.equal(graphProjectionRegistry.workspace.edges.length, 7);

  assert.equal(graphProjectionRegistry.displays.nodes.length, 7);
  assert.equal(graphProjectionRegistry.displays.edges.length, 4);
});
