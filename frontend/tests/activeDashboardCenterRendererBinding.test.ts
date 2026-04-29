import assert from "node:assert/strict";
import test from "node:test";

import {
  buildActiveDashboardCenterRendererBinding,
} from "../react_flow_preview/src/activeDashboardCenterRendererBinding.js";

test("graph renderer works", () => {
  const r = buildActiveDashboardCenterRendererBinding("topology_graph");

  assert.equal(r.resolved, true);
  assert.equal(r.rendererKind, "react_flow_graph_renderer");
  assert.equal(r.graphNodeCount > 0, true);
});

test("chart renderer works", () => {
  const r = buildActiveDashboardCenterRendererBinding("node_resources_chart");

  assert.equal(r.resolved, true);
  assert.equal(r.rendererKind, "echarts_chart_renderer");
  assert.equal(r.chartOptionAvailable, true);
});

test("unknown surface stays safe", () => {
  const r = buildActiveDashboardCenterRendererBinding("unknown_surface");

  assert.equal(r.resolved, false);
  assert.equal(r.rendererKind, "not_ready");
});
