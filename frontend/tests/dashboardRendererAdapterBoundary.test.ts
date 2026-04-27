import assert from "node:assert/strict";
import test from "node:test";

import {
  getDashboardSkeletonSurfaceById,
  getDashboardSkeletonSurfaces,
} from "../react_flow_preview/src/dashboardSkeletonSurfaceTaxonomy.js";
import {
  getDashboardRendererAdapters,
  resolveDashboardRendererAdapterForSurface,
  validateDashboardRendererAdapterRegistry,
} from "../react_flow_preview/src/dashboardRendererAdapterBoundary.js";

test("dashboard renderer adapter registry validates boundary-only adapters", () => {
  const validation = validateDashboardRendererAdapterRegistry();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);

  for (const adapter of getDashboardRendererAdapters()) {
    assert.equal(adapter.appTsxHardcodingAllowed, false);
    assert.equal(adapter.directEngineBindingAllowed, false);
    assert.equal(adapter.bindingPolicy, "adapter_boundary_only");
  }
});

test("dashboard renderer adapter boundary resolves every skeleton surface", () => {
  for (const surface of getDashboardSkeletonSurfaces()) {
    const resolution = resolveDashboardRendererAdapterForSurface(surface);

    assert.equal(resolution.resolved, true);
    assert.equal(resolution.surface.surfaceId, surface.surfaceId);
    assert.equal(
      resolution.adapter.supportedRenderModes.includes(surface.renderMode),
      true,
    );
    assert.equal(
      resolution.adapter.supportedTargetZones.includes(surface.targetZone),
      true,
    );
  }
});

test("dashboard renderer adapter boundary resolves 3d engineering surface", () => {
  const surface = getDashboardSkeletonSurfaceById("engineering_3d_cad_cam");

  if (!surface) {
    throw new Error("expected engineering_3d_cad_cam surface");
  }

  const resolution = resolveDashboardRendererAdapterForSurface(surface);

  assert.equal(resolution.adapter.adapterId, "three_d_scene_renderer");
  assert.equal(resolution.adapter.adapterKind, "three_d_scene_renderer");
  assert.equal(resolution.adapter.directEngineBindingAllowed, false);
  assert.equal(resolution.adapter.bindingPolicy, "adapter_boundary_only");
});

test("dashboard renderer adapter boundary resolves simulation and robotics surfaces", () => {
  const surfaceIds = [
    "simulation_dashboards_pack",
    "physics_digital_twin_dashboards",
    "industrial_robotics_dashboards",
    "robotics_control",
  ];

  for (const surfaceId of surfaceIds) {
    const surface = getDashboardSkeletonSurfaceById(surfaceId);

    if (!surface) {
      throw new Error(`expected surface: ${surfaceId}`);
    }

    const resolution = resolveDashboardRendererAdapterForSurface(surface);

    assert.equal(resolution.adapter.adapterId, "simulation_scene_renderer");
    assert.equal(resolution.adapter.adapterKind, "simulation_scene_renderer");
    assert.equal(resolution.adapter.directEngineBindingAllowed, false);
  }
});

test("dashboard renderer adapter boundary resolves memory control dashboard", () => {
  const surface = getDashboardSkeletonSurfaceById("memory_control_dashboard");

  if (!surface) {
    throw new Error("expected memory_control_dashboard surface");
  }

  const resolution = resolveDashboardRendererAdapterForSurface(surface);

  assert.equal(resolution.adapter.adapterId, "memory_map_renderer");
  assert.equal(resolution.adapter.adapterKind, "memory_map_renderer");
  assert.equal(resolution.adapter.directEngineBindingAllowed, false);
});
