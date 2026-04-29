import assert from "node:assert/strict";
import test from "node:test";

import {
  buildLeftDrawerSkeletonNavigationExposureReadModel,
  getLeftDrawerSkeletonNavigationExposureItemBySurfaceId,
  validateLeftDrawerSkeletonNavigationExposureReadModel,
} from "../react_flow_preview/src/leftDrawerSkeletonNavigationExposure.js";

test("left drawer skeleton navigation exposure exposes all sections and items", () => {
  const readModel = buildLeftDrawerSkeletonNavigationExposureReadModel();

  assert.equal(readModel.target, "left_dashboard_drawer");
  assert.equal(
    readModel.source,
    "dashboard_skeleton_navigation_renderer_route_binding",
  );
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 38);
  assert.equal(readModel.appTsxHardcodingAllowed, false);
});

test("left drawer skeleton navigation exposure validates stable exposure model", () => {
  const validation = validateLeftDrawerSkeletonNavigationExposureReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("left drawer skeleton navigation exposure keeps memory and mobile visible", () => {
  const readModel = buildLeftDrawerSkeletonNavigationExposureReadModel();

  assert.equal(readModel.memoryItems, 4);
  assert.equal(readModel.mobileItems, 2);

  const memoryItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "memory_control_dashboard",
  );
  const androidItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "mobile_companion_android",
  );
  const iosItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "mobile_companion_ios",
  );

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard exposure item");
  }

  if (!androidItem) {
    throw new Error("expected mobile_companion_android exposure item");
  }

  if (!iosItem) {
    throw new Error("expected mobile_companion_ios exposure item");
  }

  assert.equal(memoryItem.badges.includes("memory"), true);
  assert.equal(androidItem.badges.includes("mobile"), true);
  assert.equal(iosItem.badges.includes("mobile"), true);
  assert.equal(androidItem.buttonGroup, "mobile");
  assert.equal(iosItem.buttonGroup, "mobile");
});

test("left drawer skeleton navigation exposure marks 3d and simulation adapter routes", () => {
  const readModel = buildLeftDrawerSkeletonNavigationExposureReadModel();

  assert.equal(readModel.adapterBoundaryItems, 5);
  assert.equal(readModel.threeDItems, 1);
  assert.equal(readModel.simulationItems, 4);

  const engineeringItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "engineering_3d_cad_cam",
  );
  const simulationItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "simulation_dashboards_pack",
  );
  const roboticsItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "industrial_robotics_dashboards",
  );

  if (!engineeringItem) {
    throw new Error("expected engineering_3d_cad_cam exposure item");
  }

  if (!simulationItem) {
    throw new Error("expected simulation_dashboards_pack exposure item");
  }

  if (!roboticsItem) {
    throw new Error("expected industrial_robotics_dashboards exposure item");
  }

  assert.equal(engineeringItem.badges.includes("three_d"), true);
  assert.equal(engineeringItem.badges.includes("adapter_boundary"), true);

  assert.equal(simulationItem.badges.includes("simulation"), true);
  assert.equal(simulationItem.badges.includes("adapter_boundary"), true);

  assert.equal(roboticsItem.badges.includes("simulation"), true);
  assert.equal(roboticsItem.badges.includes("adapter_boundary"), true);
});

test("left drawer skeleton navigation exposure preserves renderer adapter ids", () => {
  const memoryItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "memory_control_dashboard",
  );
  const graphItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "topology_graph",
  );
  const chartItem = getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
    "node_resources_chart",
  );

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard exposure item");
  }

  if (!graphItem) {
    throw new Error("expected topology_graph exposure item");
  }

  if (!chartItem) {
    throw new Error("expected node_resources_chart exposure item");
  }

  assert.equal(memoryItem.rendererAdapterId, "memory_map_renderer");
  assert.equal(graphItem.rendererAdapterId, "react_flow_graph_renderer");
  assert.equal(chartItem.rendererAdapterId, "echarts_chart_renderer");
});
