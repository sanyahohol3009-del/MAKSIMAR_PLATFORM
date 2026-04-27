import assert from "node:assert/strict";
import test from "node:test";

import {
  buildAppShellPermanentRailSlotContract,
  validateAppShellPermanentRailSlotContract,
} from "../react_flow_preview/src/appShellPermanentRailSlotContract.js";

test("AppShell permanent rail slot contract exposes stable slot", () => {
  const contract = buildAppShellPermanentRailSlotContract();

  assert.equal(contract.target, "appshell_permanent_rail_slot_contract");
  assert.equal(
    contract.source,
    "permanent_dashboard_navigation_rail_shell_integration_boundary",
  );
  assert.equal(contract.host, "AppShell");
  assert.equal(contract.slotId, "left_permanent_navigation_rail_slot");
  assert.equal(contract.placement, "before_center_viewport");
  assert.equal(contract.componentExportName, "PermanentDashboardNavigationRail");
});

test("AppShell permanent rail slot contract validates cleanly", () => {
  const validation = validateAppShellPermanentRailSlotContract();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("AppShell permanent rail slot contract protects layout semantics", () => {
  const contract = buildAppShellPermanentRailSlotContract();

  assert.equal(contract.persistent, true);
  assert.equal(contract.overlay, false);
  assert.equal(contract.drawer, false);
  assert.equal(contract.centerViewportOverlapAllowed, false);
  assert.equal(contract.centerPolicy, "reserve_width_before_center_viewport");
  assert.equal(contract.overlayPolicy, "not_overlay_not_drawer");
  assert.equal(
    contract.contextualDrawerPolicy,
    "contextual_drawers_remain_active_dashboard_only",
  );
  assert.equal(
    contract.topCommunicationPolicy,
    "top_chat_remains_fullscreen_separate",
  );
});

test("AppShell permanent rail slot contract forbids manual wiring", () => {
  const contract = buildAppShellPermanentRailSlotContract();

  assert.equal(contract.appTsxHardcodingAllowed, false);
  assert.equal(contract.directDashboardButtonHardcodingAllowed, false);
  assert.equal(contract.manualDashboardTaxonomyAllowed, false);
  assert.equal(contract.manualRendererRouteLogicAllowed, false);
});

test("AppShell permanent rail slot contract carries integration boundary read model", () => {
  const contract = buildAppShellPermanentRailSlotContract({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(contract.compactWidthPx, 104);
  assert.equal(contract.expandedWidthPx, 284);
  assert.equal(
    contract.integrationBoundary.shellReadModel.activeSurfaceId,
    "engineering_3d_cad_cam",
  );
  assert.equal(contract.integrationBoundary.shellReadModel.density, "expanded");
  assert.equal(contract.integrationBoundary.shellReadModel.totalSections, 19);
  assert.equal(contract.integrationBoundary.shellReadModel.totalItems, 34);
  assert.equal(contract.integrationBoundary.shellReadModel.selectedItems, 1);
});
