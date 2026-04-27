import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentDashboardNavigationRailVisualWiringReadModel,
  getPermanentDashboardNavigationRailVisualItemBySurfaceId,
  validatePermanentDashboardNavigationRailVisualWiringReadModel,
} from "../react_flow_preview/src/permanentDashboardNavigationRailVisualWiring.js";

test("permanent dashboard navigation rail visual wiring exposes persistent left rail", () => {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel();

  assert.equal(readModel.target, "permanent_left_dashboard_navigation_rail");
  assert.equal(readModel.source, "permanent_dashboard_navigation_rail_read_model");
  assert.equal(readModel.placement, "left_permanent_rail");
  assert.equal(readModel.density, "compact");
  assert.equal(readModel.persistent, true);
  assert.equal(readModel.overlay, false);
  assert.equal(readModel.centerViewportOverlapAllowed, false);
  assert.equal(readModel.drawerSemanticsAllowedForMainDashboardList, false);
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 34);
});

test("permanent dashboard navigation rail visual wiring validates canonical model", () => {
  const validation = validatePermanentDashboardNavigationRailVisualWiringReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent dashboard navigation rail visual wiring selects default operator home", () => {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel();

  assert.equal(readModel.activeSurfaceId, "operator_home");
  assert.equal(readModel.selectedItems, 1);

  const selectedItems = readModel.sections
    .flatMap((section) => section.items)
    .filter((item) => item.selected);

  assert.equal(selectedItems.length, 1);
  assert.equal(selectedItems[0]?.surfaceId, "operator_home");
});

test("permanent dashboard navigation rail visual wiring can select 3d dashboard", () => {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(readModel.activeSurfaceId, "engineering_3d_cad_cam");
  assert.equal(readModel.density, "expanded");
  assert.equal(readModel.selectedItems, 1);
  assert.equal(readModel.threeDItems, 1);
  assert.equal(readModel.simulationItems, 4);

  const engineeringItem = getPermanentDashboardNavigationRailVisualItemBySurfaceId(
    "engineering_3d_cad_cam",
  );

  if (!engineeringItem) {
    throw new Error("expected engineering_3d_cad_cam visual item");
  }

  assert.equal(engineeringItem.visualKind, "three_d");
  assert.equal(engineeringItem.rendererAdapterId, "three_d_scene_renderer");
});

test("permanent dashboard navigation rail visual wiring preserves memory and mobile visual kinds", () => {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel();

  assert.equal(readModel.memoryItems, 4);
  assert.equal(readModel.mobileItems, 2);

  const memoryItem = getPermanentDashboardNavigationRailVisualItemBySurfaceId(
    "memory_control_dashboard",
  );
  const androidItem = getPermanentDashboardNavigationRailVisualItemBySurfaceId(
    "mobile_companion_android",
  );
  const iosItem = getPermanentDashboardNavigationRailVisualItemBySurfaceId(
    "mobile_companion_ios",
  );

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard visual item");
  }

  if (!androidItem) {
    throw new Error("expected mobile_companion_android visual item");
  }

  if (!iosItem) {
    throw new Error("expected mobile_companion_ios visual item");
  }

  assert.equal(memoryItem.visualKind, "memory");
  assert.equal(androidItem.visualKind, "mobile");
  assert.equal(iosItem.visualKind, "mobile");
});

test("permanent dashboard navigation rail visual wiring falls back to operator home for unknown surface", () => {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel({
    activeSurfaceId: "missing_surface",
  });

  assert.equal(readModel.activeSurfaceId, "operator_home");
  assert.equal(readModel.selectedItems, 1);
});
