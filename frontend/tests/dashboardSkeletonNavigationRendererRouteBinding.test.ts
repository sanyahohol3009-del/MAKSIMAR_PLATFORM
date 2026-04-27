import assert from "node:assert/strict";
import test from "node:test";

import {
  buildDashboardSkeletonNavigationRendererRouteBindingReadModel,
  getDashboardSkeletonNavigationRendererRouteBySurfaceId,
  validateDashboardSkeletonNavigationRendererRouteBindingReadModel,
} from "../react_flow_preview/src/dashboardSkeletonNavigationRendererRouteBinding.js";

test("dashboard skeleton navigation-to-renderer route binding exposes all navigation items", () => {
  const readModel =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel();

  assert.equal(readModel.source, "dashboard_skeleton_navigation_binding");
  assert.equal(readModel.navigationReadModel.totalSections, 19);
  assert.equal(readModel.navigationReadModel.totalItems, 34);
  assert.equal(readModel.totalRoutes, 34);
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.directEngineBindingAllowed, false);
});

test("dashboard skeleton navigation-to-renderer route binding validates route model", () => {
  const validation =
    validateDashboardSkeletonNavigationRendererRouteBindingReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("dashboard skeleton navigation-to-renderer route binding resolves 3d and simulation adapters", () => {
  const readModel =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel();

  assert.equal(readModel.adapterBoundaryRoutes, 5);
  assert.equal(readModel.threeDRendererRoutes, 1);
  assert.equal(readModel.simulationRendererRoutes, 4);

  const engineeringRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "engineering_3d_cad_cam",
    );

  const simulationRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "simulation_dashboards_pack",
    );

  if (!engineeringRoute) {
    throw new Error("expected engineering_3d_cad_cam route");
  }

  if (!simulationRoute) {
    throw new Error("expected simulation_dashboards_pack route");
  }

  assert.equal(
    engineeringRoute.rendererAdapter.adapterId,
    "three_d_scene_renderer",
  );
  assert.equal(
    simulationRoute.rendererAdapter.adapterId,
    "simulation_scene_renderer",
  );
  assert.equal(engineeringRoute.directEngineBindingAllowed, false);
  assert.equal(simulationRoute.directEngineBindingAllowed, false);
});

test("dashboard skeleton navigation-to-renderer route binding resolves memory map renderer", () => {
  const readModel =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel();

  assert.equal(readModel.memoryRendererRoutes, 2);

  const memoryControlRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "memory_control_dashboard",
    );

  const memoryLayersRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "memory_layers_map",
    );

  if (!memoryControlRoute) {
    throw new Error("expected memory_control_dashboard route");
  }

  if (!memoryLayersRoute) {
    throw new Error("expected memory_layers_map route");
  }

  assert.equal(
    memoryControlRoute.rendererAdapter.adapterId,
    "memory_map_renderer",
  );
  assert.equal(
    memoryLayersRoute.rendererAdapter.adapterId,
    "memory_map_renderer",
  );
});

test("dashboard skeleton navigation-to-renderer route binding resolves mobile companion routes", () => {
  const androidRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "mobile_companion_android",
    );

  const iosRoute =
    getDashboardSkeletonNavigationRendererRouteBySurfaceId(
      "mobile_companion_ios",
    );

  if (!androidRoute) {
    throw new Error("expected mobile_companion_android route");
  }

  if (!iosRoute) {
    throw new Error("expected mobile_companion_ios route");
  }

  assert.equal(androidRoute.navigationItem.buttonGroup, "mobile");
  assert.equal(iosRoute.navigationItem.buttonGroup, "mobile");
  assert.equal(androidRoute.rendererAdapter.adapterId, "react_flow_graph_renderer");
  assert.equal(iosRoute.rendererAdapter.adapterId, "react_flow_graph_renderer");
});
