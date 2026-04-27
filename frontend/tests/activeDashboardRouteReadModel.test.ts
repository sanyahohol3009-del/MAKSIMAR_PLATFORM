import assert from "node:assert/strict";
import test from "node:test";

import {
  buildActiveDashboardRouteReadModel,
} from "../react_flow_preview/src/activeDashboardRouteReadModel.js";

test("active dashboard route read model resolves graph view", () => {
  const route = buildActiveDashboardRouteReadModel("graph:topology");

  assert.equal(route.activeView, "graph:topology");
  assert.equal(route.activeKind, "graph");
  assert.equal(route.activeGraphViewKey, "topology");
  assert.equal(route.activeChartViewKey, null);
  assert.equal(typeof route.activeEntry.title, "string");
});

test("active dashboard route read model resolves chart view", () => {
  const route = buildActiveDashboardRouteReadModel("chart:node_resources");

  assert.equal(route.activeView, "chart:node_resources");
  assert.equal(route.activeKind, "chart");
  assert.equal(route.activeGraphViewKey, null);
  assert.equal(route.activeChartViewKey, "node_resources");
  assert.equal(typeof route.activeEntry.title, "string");
});
