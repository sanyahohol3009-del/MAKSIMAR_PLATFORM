import test from "node:test";
import assert from "node:assert/strict";

import {
  canonicalGraphRegistry,
  getCanonicalGraphRegistryGroups,
} from "../react_flow_preview/src/canonicalGraphRegistry.js";
import { graphProjectionRegistry } from "../react_flow_preview/src/graphProjectionData.js";

test("canonical registry counts align with projection registry", () => {
  for (const entry of canonicalGraphRegistry) {
    const projection = graphProjectionRegistry[entry.viewKey];

    assert.equal(entry.nodeCount, projection.nodes.length);
    assert.equal(entry.edgeCount, projection.edges.length);
    assert.equal(entry.title, projection.title);
    assert.equal(entry.subtitle, projection.subtitle);
  }
});

test("canonical registry groups preserve verified family split", () => {
  const groups = getCanonicalGraphRegistryGroups();

  assert.deepEqual(
    groups.map((group) => group.group),
    [
      "execution_graphs",
      "operator_graphs",
      "foundation_graphs",
      "display_graphs",
    ],
  );

  assert.deepEqual(groups[0]?.viewKeys, [
    "topology",
    "dependency",
    "dataflow",
  ]);

  assert.deepEqual(groups[1]?.viewKeys, ["modules"]);
  assert.deepEqual(groups[2]?.viewKeys, ["guard_chain", "truth_consistency"]);
  assert.deepEqual(groups[3]?.viewKeys, ["workspace", "displays"]);
});
