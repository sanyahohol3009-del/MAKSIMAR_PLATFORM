import test from "node:test";
import assert from "node:assert/strict";

import {
  canonicalGraphRegistry,
  getCanonicalGraphRegistryEntry,
  getCanonicalGraphViewOrder,
} from "../react_flow_preview/src/canonicalGraphRegistry.js";

test("canonical graph registry exposes stable ordered view keys", () => {
  assert.deepEqual(getCanonicalGraphViewOrder(), [
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

test("canonical graph registry contains eight entries", () => {
  assert.equal(canonicalGraphRegistry.length, 8);
});

test("canonical graph registry exposes truth consistency entry", () => {
  const entry = getCanonicalGraphRegistryEntry("truth_consistency");

  assert.equal(entry.title, "Truth Consistency Graph");
  assert.equal(entry.group, "foundation_graphs");
  assert.equal(entry.nodeCount, 4);
  assert.equal(entry.edgeCount, 3);
});
