import assert from "node:assert/strict";
import test from "node:test";

import {
  resolveCenterViewportForSurface,
} from "../react_flow_preview/src/activeDashboardCenterViewportBinding.js";

test("center viewport binding resolves topology graph", () => {
  const result = resolveCenterViewportForSurface("topology_graph");

  assert.equal(result.resolved, true);
  assert.equal(result.viewId, "graph:topology");
});

test("center viewport binding resolves chart", () => {
  const result = resolveCenterViewportForSurface("node_resources_chart");

  assert.equal(result.resolved, true);
  assert.equal(result.viewId, "chart:node_resources");
});

test("center viewport binding returns not resolved for unknown surface", () => {
  const result = resolveCenterViewportForSurface("unknown_surface");

  assert.equal(result.resolved, false);
});
