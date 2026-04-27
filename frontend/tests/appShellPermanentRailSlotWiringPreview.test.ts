import assert from "node:assert/strict";
import test from "node:test";

import {
  buildAppShellPermanentRailSlotWiringPreview,
  validateAppShellPermanentRailSlotWiringPreview,
} from "../react_flow_preview/src/appShellPermanentRailSlotWiringPreview.js";

test("AppShell permanent rail slot wiring preview exposes stable preview model", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview();

  assert.equal(preview.target, "appshell_permanent_rail_slot_wiring_preview");
  assert.equal(preview.source, "appshell_permanent_rail_slot_contract");
  assert.equal(preview.host, "AppShell");
  assert.equal(preview.status, "preview_ready");
  assert.equal(preview.railSlot.slotId, "left_permanent_navigation_rail_slot");
  assert.equal(preview.railSlot.componentExportName, "PermanentDashboardNavigationRail");
});

test("AppShell permanent rail slot wiring preview validates cleanly", () => {
  const validation = validateAppShellPermanentRailSlotWiringPreview();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("AppShell permanent rail slot wiring preview keeps rail non-overlay and non-drawer", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview();

  assert.equal(preview.railSlot.persistent, true);
  assert.equal(preview.railSlot.overlay, false);
  assert.equal(preview.railSlot.drawer, false);
  assert.equal(preview.railSlot.centerViewportOverlapAllowed, false);
  assert.equal(preview.railSlot.placement, "before_center_viewport");
  assert.equal(preview.centerViewportSlot.placement, "after_left_permanent_navigation_rail");
  assert.equal(preview.centerViewportSlot.widthPolicy, "remaining_shell_width");
  assert.equal(preview.centerViewportSlot.railMayOverlap, false);
});

test("AppShell permanent rail slot wiring preview keeps contextual drawers active-dashboard-only", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview();

  assert.equal(preview.contextualDrawers.policy, "active_dashboard_only");
  assert.equal(preview.contextualDrawers.mayContainMainDashboardList, false);
  assert.equal(
    preview.contextualDrawers.leftContextualDrawer,
    "active_dashboard_functions_settings_tools",
  );
  assert.equal(
    preview.contextualDrawers.rightContextualDrawer,
    "active_dashboard_state_diagnostics_context",
  );
});

test("AppShell permanent rail slot wiring preview keeps top chat separate", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview();

  assert.equal(preview.topCommunication.policy, "fullscreen_chat_separate");
  assert.equal(preview.topCommunication.mayContainDashboardNavigation, false);
  assert.equal(preview.topCommunication.topCommunicationDrawer, "fullscreen_jarvis_chat");
});

test("AppShell permanent rail slot wiring preview forbids manual UI wiring", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview();

  assert.equal(preview.appTsxModificationAllowed, false);
  assert.equal(preview.appTsxHardcodingAllowed, false);
  assert.equal(preview.manualDashboardButtonListAllowed, false);
  assert.equal(preview.manualRendererRouteLogicAllowed, false);
  assert.equal(preview.manualTaxonomyDuplicationAllowed, false);
});

test("AppShell permanent rail slot wiring preview resolves expanded width for expanded rail", () => {
  const preview = buildAppShellPermanentRailSlotWiringPreview({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(preview.railSlot.widthPx, 284);
  assert.equal(
    preview.contract.integrationBoundary.shellReadModel.activeSurfaceId,
    "engineering_3d_cad_cam",
  );
  assert.equal(preview.contract.integrationBoundary.shellReadModel.density, "expanded");
});
