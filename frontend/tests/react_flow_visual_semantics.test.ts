import test from "node:test";
import assert from "node:assert/strict";

import {
  buildStyledEdges,
  buildStyledNodes,
} from "../react_flow_preview/src/graphVisualSemantics.js";

test("styled topology nodes preserve total count", () => {
  const nodes = buildStyledNodes("topology");

  assert.equal(nodes.length, 3);
  assert.equal(Boolean(nodes[0]?.style), true);
});

test("styled dataflow edges preserve total count", () => {
  const edges = buildStyledEdges("dataflow");

  assert.equal(edges.length, 5);
  assert.equal(edges.some((edge) => edge.animated === true), true);
});

test("styled module nodes remain present", () => {
  const nodes = buildStyledNodes("modules");

  assert.equal(nodes.length, 3);
  assert.equal(
    nodes.some((node) => typeof node.data?.label === "string"),
    true,
  );
});

test("styled guard chain nodes remain present", () => {
  const nodes = buildStyledNodes("guard_chain");

  assert.equal(nodes.length, 4);
});

test("styled display assignment edges remain present", () => {
  const edges = buildStyledEdges("displays");

  assert.equal(edges.length, 4);
  assert.equal(edges.some((edge) => edge.animated === true), true);
});
