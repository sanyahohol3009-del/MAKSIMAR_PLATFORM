import assert from "node:assert/strict";
import test from "node:test";

import {
  getDashboardSkeletonSurfaceById,
  getDashboardSkeletonSurfaces,
  getMemoryControlSurfaces,
  getMobileCompanionSurfaces,
  getReservedAdapterSurfaces,
  groupDashboardSkeletonSurfacesByButtonGroup,
  validateDashboardSkeletonSurfaceTaxonomy,
} from "../react_flow_preview/src/dashboardSkeletonSurfaceTaxonomy.js";

test("dashboard skeleton taxonomy exposes expanded dashboard button groups", () => {
  const groups = groupDashboardSkeletonSurfacesByButtonGroup();

  assert.equal(groups.length, 19);
  assert.deepEqual(
    groups.map((group) => group.buttonGroup),
    [
      "home",
      "foundation",
      "incidents",
      "graphs",
      "telemetry",
      "interaction",
      "memory",
      "project_context",
      "server",
      "security",
      "family",
      "mobile",
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
  assert.equal(getDashboardSkeletonSurfaces().length, 34);
});

test("dashboard skeleton taxonomy includes audit 122 dashboard surfaces", () => {
  const requiredSurfaceIds = [
    "foundation_unified_dashboard",
    "foundation_incident_dashboard",
    "foundation_diagnostics_correlation",
    "dependency_graph",
    "dataflow_graph",
    "displays_graph",
    "action_queue_panel",
    "approval_queue_panel",
    "audit_timeline_panel",
    "project_context_surface",
    "base_family_dashboard",
    "physics_digital_twin_dashboards",
    "industrial_robotics_dashboards",
  ];

  for (const surfaceId of requiredSurfaceIds) {
    const surface = getDashboardSkeletonSurfaceById(surfaceId);

    if (!surface) {
      throw new Error(`expected surface: ${surfaceId}`);
    }

    assert.equal(surface.surfaceId, surfaceId);
  }
});

test("dashboard skeleton taxonomy separates android and ios from family", () => {
  const mobileSurfaces = getMobileCompanionSurfaces();

  assert.deepEqual(
    mobileSurfaces.map((surface) => surface.surfaceId),
    ["mobile_companion_android", "mobile_companion_ios"],
  );

  for (const surface of mobileSurfaces) {
    assert.equal(surface.domain, "mobile_companion");
    assert.equal(surface.buttonGroup, "mobile");
  }
});

test("dashboard skeleton taxonomy exposes memory control surfaces", () => {
  const memorySurfaces = getMemoryControlSurfaces();

  assert.deepEqual(
    memorySurfaces.map((surface) => surface.surfaceId),
    [
      "memory_control_dashboard",
      "memory_layers_map",
      "memory_folder_sequence",
      "memory_governance_policy",
    ],
  );

  for (const surface of memorySurfaces) {
    assert.equal(surface.domain, "memory_governance");
    assert.equal(surface.buttonGroup, "memory");
  }
});

test("dashboard skeleton taxonomy reserves 3d and simulation adapter surfaces", () => {
  const adapterSurfaces = getReservedAdapterSurfaces();

  assert.deepEqual(
    adapterSurfaces.map((surface) => surface.surfaceId),
    [
      "simulation_dashboards_pack",
      "physics_digital_twin_dashboards",
      "industrial_robotics_dashboards",
      "robotics_control",
      "engineering_3d_cad_cam",
    ],
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
