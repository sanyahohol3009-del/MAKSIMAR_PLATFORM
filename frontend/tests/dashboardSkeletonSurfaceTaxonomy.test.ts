import assert from "node:assert/strict";
import test from "node:test";

import {
  getDashboardSkeletonSurfaceById,
  getDashboardSkeletonSurfaces,
  getReservedAdapterSurfaces,
  groupDashboardSkeletonSurfacesByButtonGroup,
  validateDashboardSkeletonSurfaceTaxonomy,
} from "../react_flow_preview/src/dashboardSkeletonSurfaceTaxonomy.js";

test("dashboard skeleton taxonomy exposes the planned dashboard button groups", () => {
  const groups = groupDashboardSkeletonSurfacesByButtonGroup();

  assert.equal(groups.length, 13);
  assert.deepEqual(
    groups.map((group) => group.buttonGroup),
    [
      "home",
      "server",
      "security",
      "memory",
      "commands",
      "family",
      "smart_home",
      "simulation",
      "robotics",
      "engineering",
      "media",
      "business",
      "settings",
    ],
  );
});

test("dashboard skeleton taxonomy keeps all surface ids stable and unique", () => {
  const validation = validateDashboardSkeletonSurfaceTaxonomy();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
  assert.equal(getDashboardSkeletonSurfaces().length, 13);
});

test("dashboard skeleton taxonomy reserves 3d and simulation adapter surfaces", () => {
  const adapterSurfaces = getReservedAdapterSurfaces();

  assert.deepEqual(
    adapterSurfaces.map((surface) => surface.surfaceId),
    ["physics_simulation", "robotics_control", "engineering_3d_cad_cam"],
  );

  for (const surface of adapterSurfaces) {
    assert.equal(surface.status, "reserved");
    assert.equal(surface.adapterBoundaryRequired, true);
    assert.equal(surface.clientSelectable, true);
  }
});

test("dashboard skeleton taxonomy exposes engineering 3d surface for future renderer", () => {
  const surface = getDashboardSkeletonSurfaceById("engineering_3d_cad_cam");

  if (!surface) {
    throw new Error("expected engineering_3d_cad_cam surface");
  }

  assert.equal(surface.title, "3D / CAD / CAM");
  assert.equal(surface.renderMode, "three_d_scene_adapter");
  assert.equal(surface.targetZone, "center_viewport");
  assert.equal(surface.adapterBoundaryRequired, true);
});
