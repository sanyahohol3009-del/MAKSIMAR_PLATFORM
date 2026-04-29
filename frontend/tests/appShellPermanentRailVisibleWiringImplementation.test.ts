import assert from "node:assert/strict";
import test from "node:test";

import { AppShell } from "../react_flow_preview/src/shell/AppShell.js";
import { PermanentDashboardNavigationRail } from "../react_flow_preview/src/permanentDashboardNavigationRailShellComponent.js";
import {
  buildAppShellPermanentRailVisibleWiringContract,
  validateAppShellPermanentRailVisibleWiringContract,
} from "../react_flow_preview/src/appShellPermanentRailVisibleWiringContract.js";
import {
  buildPermanentDashboardNavigationRailShellReadModel,
} from "../react_flow_preview/src/permanentDashboardNavigationRailShellComponent.js";

test("AppShell permanent rail visible wiring implementation keeps component exports available", () => {
  assert.equal(typeof AppShell, "function");
  assert.equal(typeof PermanentDashboardNavigationRail, "function");
});

test("AppShell permanent rail visible wiring implementation keeps visible wiring contract valid", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract();
  const validation = validateAppShellPermanentRailVisibleWiringContract(contract);

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
  assert.equal(contract.visibleWiringAllowed, true);
  assert.equal(contract.dedicatedShellSlotRequired, true);
  assert.equal(contract.readModelDriven, true);
});

test("AppShell permanent rail visible wiring implementation preserves shell slot model", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract();

  assert.equal(contract.railSlot.slotId, "left_permanent_navigation_rail_slot");
  assert.equal(contract.railSlot.componentExportName, "PermanentDashboardNavigationRail");
  assert.equal(contract.railSlot.placement, "before_center_viewport");
  assert.equal(contract.railSlot.persistent, true);
  assert.equal(contract.railSlot.overlay, false);
  assert.equal(contract.railSlot.drawer, false);
  assert.equal(contract.railSlot.mayOverlapCenterViewport, false);

  assert.equal(contract.centerViewportSlot.slotId, "center_dashboard_viewport_slot");
  assert.equal(
    contract.centerViewportSlot.placement,
    "after_left_permanent_navigation_rail",
  );
  assert.equal(contract.centerViewportSlot.widthPolicy, "remaining_shell_width");
});

test("AppShell permanent rail visible wiring implementation remains read-model driven", () => {
  const readModel = buildPermanentDashboardNavigationRailShellReadModel({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(readModel.target, "permanent_dashboard_navigation_rail_shell_component");
  assert.equal(readModel.activeSurfaceId, "engineering_3d_cad_cam");
  assert.equal(readModel.density, "expanded");
  assert.equal(readModel.totalSections, 19);
  assert.equal(readModel.totalItems, 38);
  assert.equal(readModel.selectedItems, 1);
  assert.equal(readModel.threeDItems, 1);
});
