import assert from "node:assert/strict";
import test from "node:test";

import {
  getDashboardSkeletonSurfaceById,
  validateDashboardSkeletonSurfaceTaxonomy,
} from "../react_flow_preview/src/dashboardSkeletonSurfaceTaxonomy.js";

test("dashboard skeleton taxonomy includes canonical graph surface expansion", () => {
  const expectedSurfaceIds = [
    "modules_graph",
    "guard_chain_graph",
    "truth_consistency_graph",
    "workspace_graph",
  ];

  for (const surfaceId of expectedSurfaceIds) {
    const surface = getDashboardSkeletonSurfaceById(surfaceId);

    if (!surface) {
      throw new Error(`missing surface: ${surfaceId}`);
    }

    assert.equal(surface.domain, "visual_graphs");
    assert.equal(surface.buttonGroup, "graphs");
    assert.equal(surface.targetZone, "center_viewport");
    assert.equal(surface.renderMode, "graph_view");
    assert.equal(surface.status, "implemented");
    assert.equal(surface.clientSelectable, true);
    assert.equal(surface.adapterBoundaryRequired, false);
  }
});

test("dashboard skeleton taxonomy remains valid after canonical graph expansion", () => {
  const validation = validateDashboardSkeletonSurfaceTaxonomy();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});
