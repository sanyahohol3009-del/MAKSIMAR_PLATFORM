import test from "node:test";
import assert from "node:assert/strict";

import { graphProjectionRegistry } from "../react_flow_preview/src/graphProjectionData.js";

test("every projection node has readable semantic payload", () => {
  for (const view of Object.values(graphProjectionRegistry)) {
    for (const node of view.nodes) {
      assert.equal(node.title.length > 0, true);
      assert.equal(node.subtitle.length > 0, true);
      assert.equal(node.semanticKind.length > 0, true);
      assert.equal(node.fields.length >= 2, true);
    }
  }
});

test("every projection edge has readable semantic payload", () => {
  for (const view of Object.values(graphProjectionRegistry)) {
    for (const edge of view.edges) {
      assert.equal(edge.title.length > 0, true);
      assert.equal(edge.semanticKind.length > 0, true);
      assert.equal(edge.fields.length >= 2, true);
      assert.equal(edge.source !== edge.target, true);
    }
  }
});
