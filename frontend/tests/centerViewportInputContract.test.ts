import assert from "node:assert/strict";
import test from "node:test";

import {
  buildActiveDashboardRouteReadModel,
} from "../react_flow_preview/src/activeDashboardRouteReadModel.js";
import {
  buildCenterViewportInputContract,
} from "../react_flow_preview/src/centerViewportInputContract.js";

test("center viewport input contract resolves graph input", () => {
  const route = buildActiveDashboardRouteReadModel("graph:topology");
  const input = buildCenterViewportInputContract(route);

  assert.equal(input.activeView, "graph:topology");
  assert.equal(input.surfaceKind, "graph");
  assert.equal(input.activeGraphViewKey, "topology");
  assert.equal(input.activeChartViewKey, null);
  assert.equal(input.centerImmutable, true);
  assert.equal(input.drawerPolicy, "overlay_only");
  assert.equal(input.rendererResponsibility, "render_only");
  assert.equal(input.routingSource, "active_dashboard_route_read_model");
});

test("center viewport input contract resolves chart input", () => {
  const route = buildActiveDashboardRouteReadModel("chart:node_resources");
  const input = buildCenterViewportInputContract(route);

  assert.equal(input.activeView, "chart:node_resources");
  assert.equal(input.surfaceKind, "chart");
  assert.equal(input.activeGraphViewKey, null);
  assert.equal(input.activeChartViewKey, "node_resources");
  assert.equal(input.centerImmutable, true);
  assert.equal(input.drawerPolicy, "overlay_only");
  assert.equal(input.rendererResponsibility, "render_only");
  assert.equal(input.routingSource, "active_dashboard_route_read_model");
});
