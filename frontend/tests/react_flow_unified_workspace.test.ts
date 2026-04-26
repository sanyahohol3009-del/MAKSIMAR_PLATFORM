import test from "node:test";
import assert from "node:assert/strict";

import {
  buildUnifiedWorkspaceSnapshot,
  getNextGraphViewKey,
  getPreviousGraphViewKey,
} from "../react_flow_preview/src/unifiedGraphWorkspace.js";

test("next graph view key follows canonical registry order", () => {
  assert.equal(getNextGraphViewKey("topology"), "dependency");
  assert.equal(getNextGraphViewKey("displays"), "topology");
});

test("previous graph view key follows canonical registry order", () => {
  assert.equal(getPreviousGraphViewKey("dependency"), "topology");
  assert.equal(getPreviousGraphViewKey("topology"), "displays");
});

test("unified workspace snapshot aggregates totals", () => {
  const snapshot = buildUnifiedWorkspaceSnapshot("guard_chain");

  assert.equal(snapshot.totalViews, 8);
  assert.equal(snapshot.totalNodes, 41);
  assert.equal(snapshot.totalEdges, 30);
  assert.equal(snapshot.activeView.viewKey, "guard_chain");
});

test("unified workspace snapshot preserves grouped registry structure", () => {
  const snapshot = buildUnifiedWorkspaceSnapshot("workspace");

  assert.deepEqual(
    snapshot.groupedViews.map((group) => group.group),
    [
      "execution_graphs",
      "operator_graphs",
      "foundation_graphs",
      "display_graphs",
    ],
  );

  assert.deepEqual(
    snapshot.groupedViews[0]?.views.map((view) => view.viewKey),
    ["topology", "dependency", "dataflow"],
  );
});
