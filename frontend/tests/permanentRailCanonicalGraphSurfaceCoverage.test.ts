import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentRailActiveDashboardSelectionBindingReadModel,
  getActiveViewForPermanentRailSurfaceId,
  getPermanentRailSelectionRouteBySurfaceId,
} from "../react_flow_preview/src/permanentRailActiveDashboardSelectionBinding.js";

test("permanent rail resolves canonical graph and chart dashboard surfaces", () => {
  const expectedMappings = new Map([
    ["operator_home", "graph:topology"],
    ["topology_graph", "graph:topology"],
    ["dependency_graph", "graph:dependency"],
    ["dataflow_graph", "graph:dataflow"],
    ["modules_graph", "graph:modules"],
    ["guard_chain_graph", "graph:guard_chain"],
    ["truth_consistency_graph", "graph:truth_consistency"],
    ["workspace_graph", "graph:workspace"],
    ["displays_graph", "graph:displays"],
    ["node_resources_chart", "chart:node_resources"],
    ["security_telemetry_chart", "chart:security_telemetry"],
    ["multi_series_summary_chart", "chart:summary"],
  ]);

  for (const [surfaceId, expectedViewId] of expectedMappings) {
    assert.equal(
      getActiveViewForPermanentRailSurfaceId(surfaceId),
      expectedViewId,
      surfaceId,
    );

    const route = getPermanentRailSelectionRouteBySurfaceId(surfaceId);

    if (!route) {
      throw new Error(`missing route for ${surfaceId}`);
    }

    assert.equal(route.routeStatus, "center_viewport_ready", surfaceId);
  }
});

test("permanent rail ready route census includes all canonical graph and chart surfaces", () => {
  const model = buildPermanentRailActiveDashboardSelectionBindingReadModel();

  const readyRoutes = model.routes
    .filter((route) => route.routeStatus === "center_viewport_ready")
    .map((route) => `${route.surfaceId}->${route.activeView}`)
    .sort();

  assert.deepEqual(
    readyRoutes,
    [
      "dataflow_graph->graph:dataflow",
      "dependency_graph->graph:dependency",
      "displays_graph->graph:displays",
      "guard_chain_graph->graph:guard_chain",
      "modules_graph->graph:modules",
      "multi_series_summary_chart->chart:summary",
      "node_resources_chart->chart:node_resources",
      "operator_home->graph:topology",
      "security_telemetry_chart->chart:security_telemetry",
      "topology_graph->graph:topology",
      "truth_consistency_graph->graph:truth_consistency",
      "workspace_graph->graph:workspace",
    ].sort(),
  );
});

test("permanent rail keeps unknown surfaces not-ready instead of guessing", () => {
  assert.equal(getActiveViewForPermanentRailSurfaceId("missing_surface"), null);
});
