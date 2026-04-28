import assert from "node:assert/strict";
import test from "node:test";

import {
  buildAppShellPermanentRailVisibleWiringContract,
  validateAppShellPermanentRailVisibleWiringContract,
} from "../react_flow_preview/src/appShellPermanentRailVisibleWiringContract.js";

test("AppShell permanent rail visible wiring contract exposes stable contract", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract();

  assert.equal(contract.target, "appshell_permanent_rail_visible_wiring_contract");
  assert.equal(contract.source, "appshell_permanent_rail_slot_wiring_preview");
  assert.equal(contract.host, "AppShell");
  assert.equal(contract.status, "visible_wiring_contract_ready");
  assert.equal(contract.wiringMode, "dedicated_shell_slot_only");
  assert.equal(contract.layoutMode, "left_rail_center_viewport_shell_grid");
});

test("AppShell permanent rail visible wiring contract validates cleanly", () => {
  const validation = validateAppShellPermanentRailVisibleWiringContract();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("AppShell permanent rail visible wiring contract preserves rail and center layout", () => {
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
  assert.equal(contract.centerViewportSlot.receivesActiveDashboardSurface, true);
  assert.equal(contract.centerViewportSlot.railMayOverlap, false);
});

test("AppShell permanent rail visible wiring contract keeps drawers and chat separated", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract();

  assert.equal(contract.contextualDrawers.policy, "active_dashboard_only");
  assert.equal(contract.contextualDrawers.leftDrawerPurpose, "functions_settings_tools");
  assert.equal(contract.contextualDrawers.rightDrawerPurpose, "state_diagnostics_context");
  assert.equal(contract.contextualDrawers.mayContainMainDashboardList, false);

  assert.equal(contract.topCommunication.policy, "fullscreen_chat_separate");
  assert.equal(contract.topCommunication.drawerPurpose, "jarvis_chat_surface");
  assert.equal(contract.topCommunication.mayContainDashboardNavigation, false);
});

test("AppShell permanent rail visible wiring contract forbids direct App.tsx hardcoding", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract();

  assert.equal(contract.visibleWiringAllowed, true);
  assert.equal(contract.appTsxDirectButtonListAllowed, false);
  assert.equal(contract.appTsxDirectRendererRouteLogicAllowed, false);
  assert.equal(contract.appTsxDirectTaxonomyDuplicationAllowed, false);
  assert.equal(contract.appTsxDirectClientGatingAllowed, false);
  assert.equal(contract.appTsxDirectDrawerSemanticRewriteAllowed, false);
  assert.equal(contract.dedicatedShellSlotRequired, true);
  assert.equal(contract.readModelDriven, true);
});

test("AppShell permanent rail visible wiring contract preserves expanded rail width", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(contract.railSlot.widthPx, 284);
  assert.equal(contract.preview.railSlot.widthPx, 284);
  assert.equal(
    contract.preview.contract.integrationBoundary.shellReadModel.activeSurfaceId,
    "engineering_3d_cad_cam",
  );
});
