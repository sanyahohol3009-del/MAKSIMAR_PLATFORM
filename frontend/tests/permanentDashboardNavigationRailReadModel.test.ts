import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentDashboardNavigationRailReadModel,
  getPermanentDashboardNavigationRailItemBySurfaceId,
  validatePermanentDashboardNavigationRailReadModel,
} from "../react_flow_preview/src/permanentDashboardNavigationRailReadModel.js";

test("permanent dashboard navigation rail exposes persistent dashboard list", () => {
  const readModel = buildPermanentDashboardNavigationRailReadModel();

  assert.equal(readModel.target, "permanent_dashboard_navigation_rail");
  assert.equal(readModel.displayMode, "persistent_left_rail");
  assert.equal(readModel.source, "left_drawer_skeleton_navigation_exposure");
  assert.equal(readModel.persistent, true);
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 38);
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.drawerSemanticsAllowedForMainDashboardList, false);
});

test("permanent dashboard navigation rail validates canonical rail model", () => {
  const validation = validatePermanentDashboardNavigationRailReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent dashboard navigation rail keeps memory and mobile in correct groups", () => {
  const readModel = buildPermanentDashboardNavigationRailReadModel();

  assert.equal(readModel.memoryItems, 4);
  assert.equal(readModel.mobileItems, 2);

  const memoryItem = getPermanentDashboardNavigationRailItemBySurfaceId(
    "memory_control_dashboard",
  );
  const androidItem = getPermanentDashboardNavigationRailItemBySurfaceId(
    "mobile_companion_android",
  );
  const iosItem = getPermanentDashboardNavigationRailItemBySurfaceId(
    "mobile_companion_ios",
  );

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard rail item");
  }

  if (!androidItem) {
    throw new Error("expected mobile_companion_android rail item");
  }

  if (!iosItem) {
    throw new Error("expected mobile_companion_ios rail item");
  }

  assert.equal(memoryItem.buttonGroup, "memory");
  assert.equal(androidItem.buttonGroup, "mobile");
  assert.equal(iosItem.buttonGroup, "mobile");
  assert.equal(memoryItem.displayMode, "persistent_left_rail");
  assert.equal(androidItem.displayMode, "persistent_left_rail");
  assert.equal(iosItem.displayMode, "persistent_left_rail");
});

test("permanent dashboard navigation rail exposes 3d and simulation entries", () => {
  const readModel = buildPermanentDashboardNavigationRailReadModel();

  assert.equal(readModel.adapterBoundaryItems, 5);
  assert.equal(readModel.threeDItems, 1);
  assert.equal(readModel.simulationItems, 4);

  const engineeringItem = getPermanentDashboardNavigationRailItemBySurfaceId(
    "engineering_3d_cad_cam",
  );
  const simulationItem = getPermanentDashboardNavigationRailItemBySurfaceId(
    "simulation_dashboards_pack",
  );

  if (!engineeringItem) {
    throw new Error("expected engineering_3d_cad_cam rail item");
  }

  if (!simulationItem) {
    throw new Error("expected simulation_dashboards_pack rail item");
  }

  assert.equal(engineeringItem.rendererAdapterId, "three_d_scene_renderer");
  assert.equal(engineeringItem.badges.includes("three_d"), true);
  assert.equal(engineeringItem.badges.includes("adapter_boundary"), true);

  assert.equal(simulationItem.rendererAdapterId, "simulation_scene_renderer");
  assert.equal(simulationItem.badges.includes("simulation"), true);
  assert.equal(simulationItem.badges.includes("adapter_boundary"), true);
});

test("permanent dashboard navigation rail preserves all canonical button groups", () => {
  const readModel = buildPermanentDashboardNavigationRailReadModel();

  assert.deepEqual(
    readModel.sections.map((section) => section.buttonGroup),
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
