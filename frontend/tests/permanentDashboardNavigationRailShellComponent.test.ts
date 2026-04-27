import assert from "node:assert/strict";
import test from "node:test";

import {
  PermanentDashboardNavigationRail,
  buildPermanentDashboardNavigationRailShellReadModel,
  getPermanentDashboardNavigationRailBadgeLabel,
  getPermanentDashboardNavigationRailItemAriaLabel,
  getPermanentDashboardNavigationRailItemShortLabel,
  validatePermanentDashboardNavigationRailShellReadModel,
} from "../react_flow_preview/src/permanentDashboardNavigationRailShellComponent.js";

test("permanent dashboard navigation rail shell read model exposes stable component contract", () => {
  const readModel = buildPermanentDashboardNavigationRailShellReadModel();

  assert.equal(readModel.target, "permanent_dashboard_navigation_rail_shell_component");
  assert.equal(readModel.source, "permanent_dashboard_navigation_rail_visual_wiring");
  assert.equal(readModel.placement, "left_permanent_rail");
  assert.equal(readModel.role, "dashboard_navigation");
  assert.equal(readModel.persistent, true);
  assert.equal(readModel.overlay, false);
  assert.equal(readModel.centerViewportOverlapAllowed, false);
  assert.equal(readModel.drawerSemanticsAllowedForMainDashboardList, false);
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 34);
  assert.equal(readModel.selectedItems, 1);
});

test("permanent dashboard navigation rail shell read model validates cleanly", () => {
  const validation = validatePermanentDashboardNavigationRailShellReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent dashboard navigation rail shell supports expanded 3d selection", () => {
  const readModel = buildPermanentDashboardNavigationRailShellReadModel({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  const selectedItems = readModel.sections
    .flatMap((section) => section.items)
    .filter((item) => item.selected);

  assert.equal(readModel.activeSurfaceId, "engineering_3d_cad_cam");
  assert.equal(readModel.density, "expanded");
  assert.equal(selectedItems.length, 1);
  assert.equal(selectedItems[0]?.surfaceId, "engineering_3d_cad_cam");
  assert.equal(selectedItems[0]?.rendererAdapterId, "three_d_scene_renderer");
});

test("permanent dashboard navigation rail presenters build readable item labels", () => {
  const readModel = buildPermanentDashboardNavigationRailShellReadModel({
    activeSurfaceId: "memory_control_dashboard",
  });

  const memoryItem = readModel.sections
    .flatMap((section) => section.items)
    .find((item) => item.surfaceId === "memory_control_dashboard");

  if (!memoryItem) {
    throw new Error("expected memory_control_dashboard shell item");
  }

  assert.equal(getPermanentDashboardNavigationRailItemShortLabel(memoryItem), "MC");
  assert.equal(
    getPermanentDashboardNavigationRailItemAriaLabel(memoryItem),
    "Memory Control Dashboard, selected, approval required, direct read model route",
  );
  assert.equal(getPermanentDashboardNavigationRailBadgeLabel("memory"), "Memory");
});

test("permanent dashboard navigation rail component is exported as render function", () => {
  assert.equal(typeof PermanentDashboardNavigationRail, "function");
});
