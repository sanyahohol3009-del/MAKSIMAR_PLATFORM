import assert from "node:assert/strict";
import test from "node:test";

import {
  buildDashboardSkeletonNavigationBindingReadModel,
  getDashboardSkeletonNavigationItemBySurfaceId,
  validateDashboardSkeletonNavigationBindingReadModel,
} from "../react_flow_preview/src/dashboardSkeletonNavigationBinding.js";

test("dashboard skeleton navigation binding exposes all taxonomy groups", () => {
  const readModel = buildDashboardSkeletonNavigationBindingReadModel();

  assert.equal(readModel.targetShell, "left_dashboard_drawer");
  assert.equal(readModel.bindingSource, "dashboard_skeleton_surface_taxonomy");
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 34);
});

test("dashboard skeleton navigation binding validates stable navigation model", () => {
  const validation = validateDashboardSkeletonNavigationBindingReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("dashboard skeleton navigation binding keeps memory and mobile separated", () => {
  const readModel = buildDashboardSkeletonNavigationBindingReadModel();

  assert.equal(readModel.memoryItems, 4);
  assert.equal(readModel.mobileItems, 2);

  const memoryItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "memory_control_dashboard",
  );
  const androidItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "mobile_companion_android",
  );
  const iosItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "mobile_companion_ios",
  );

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard navigation item");
  }

  if (!androidItem) {
    throw new Error("expected mobile_companion_android navigation item");
  }

  if (!iosItem) {
    throw new Error("expected mobile_companion_ios navigation item");
  }

  assert.equal(memoryItem.buttonGroup, "memory");
  assert.equal(androidItem.buttonGroup, "mobile");
  assert.equal(iosItem.buttonGroup, "mobile");
});

test("dashboard skeleton navigation binding exposes adapter surfaces as navigation items", () => {
  const readModel = buildDashboardSkeletonNavigationBindingReadModel();

  assert.equal(readModel.adapterBoundaryItems, 5);

  const engineeringItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "engineering_3d_cad_cam",
  );
  const simulationItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "simulation_dashboards_pack",
  );
  const roboticsItem = getDashboardSkeletonNavigationItemBySurfaceId(
    "industrial_robotics_dashboards",
  );

  if (!engineeringItem) {
    throw new Error("expected engineering_3d_cad_cam navigation item");
  }

  if (!simulationItem) {
    throw new Error("expected simulation_dashboards_pack navigation item");
  }

  if (!roboticsItem) {
    throw new Error("expected industrial_robotics_dashboards navigation item");
  }

  assert.equal(engineeringItem.adapterBoundaryRequired, true);
  assert.equal(engineeringItem.renderMode, "three_d_scene_adapter");
  assert.equal(simulationItem.adapterBoundaryRequired, true);
  assert.equal(simulationItem.renderMode, "simulation_scene_adapter");
  assert.equal(roboticsItem.adapterBoundaryRequired, true);
  assert.equal(roboticsItem.renderMode, "simulation_scene_adapter");
});
