import test from "node:test";
import assert from "node:assert/strict";
import {
  buildUnifiedVisualWorkspaceSnapshot,
  getNextUnifiedVisualViewId,
  getPreviousUnifiedVisualViewId,
} from "../react_flow_preview/src/unifiedVisualWorkspace.js";

test("next unified visual view crosses graph-to-chart boundary", () => {
  assert.equal(
    getNextUnifiedVisualViewId("graph:displays"),
    "chart:node_resources",
  );
});

test("previous unified visual view crosses chart-to-graph boundary", () => {
  assert.equal(
    getPreviousUnifiedVisualViewId("chart:node_resources"),
    "graph:displays",
  );
});

test("unified visual workspace snapshot aggregates graph and chart views", () => {
  const snapshot = buildUnifiedVisualWorkspaceSnapshot("chart:summary");
  assert.equal(snapshot.totalViews, 12);
  assert.equal(snapshot.totalGraphViews, 8);
  assert.equal(snapshot.totalChartViews, 4);
  assert.equal(snapshot.activeView.viewKind, "chart");
  assert.equal(snapshot.activeView.viewId, "chart:summary");
  assert.equal(snapshot.groupedViews.at(-1)?.group, "telemetry_charts");
  assert.equal(snapshot.groupedViews.at(-1)?.views.length, 4);
});
