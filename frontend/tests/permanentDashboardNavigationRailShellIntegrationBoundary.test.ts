import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentDashboardNavigationRailShellIntegrationBoundary,
  validatePermanentDashboardNavigationRailShellIntegrationBoundary,
} from "../react_flow_preview/src/permanentDashboardNavigationRailShellIntegrationBoundary.js";

test("permanent dashboard navigation rail shell integration boundary exposes stable shell slot", () => {
  const boundary = buildPermanentDashboardNavigationRailShellIntegrationBoundary();

  assert.equal(
    boundary.target,
    "permanent_dashboard_navigation_rail_shell_integration_boundary",
  );
  assert.equal(boundary.source, "permanent_dashboard_navigation_rail_shell_component");
  assert.equal(boundary.host, "operator_dashboard_shell");
  assert.equal(boundary.slot, "left_permanent_navigation_rail_slot");
  assert.equal(boundary.placement, "left_permanent_rail");
  assert.equal(boundary.componentExportName, "PermanentDashboardNavigationRail");
});

test("permanent dashboard navigation rail shell integration boundary validates cleanly", () => {
  const validation =
    validatePermanentDashboardNavigationRailShellIntegrationBoundary();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent dashboard navigation rail shell integration boundary protects layout semantics", () => {
  const boundary = buildPermanentDashboardNavigationRailShellIntegrationBoundary();

  assert.equal(boundary.layoutContract.persistent, true);
  assert.equal(boundary.layoutContract.overlay, false);
  assert.equal(boundary.layoutContract.centerViewportOverlapAllowed, false);
  assert.equal(
    boundary.layoutContract.drawerSemanticsAllowedForMainDashboardList,
    false,
  );
  assert.equal(boundary.layoutContract.contextualDrawerPolicy, "active_dashboard_only");
  assert.equal(boundary.layoutContract.topCommunicationPolicy, "fullscreen_chat_separate");
  assert.equal(boundary.layoutContract.compactWidthPx, 104);
  assert.equal(boundary.layoutContract.expandedWidthPx, 284);
});

test("permanent dashboard navigation rail shell integration boundary keeps App.tsx hardcoding forbidden", () => {
  const boundary = buildPermanentDashboardNavigationRailShellIntegrationBoundary();

  assert.equal(boundary.appTsxHardcodingAllowed, false);
  assert.equal(boundary.directDashboardButtonHardcodingAllowed, false);
  assert.equal(boundary.directDrawerSemanticsAllowed, false);
});

test("permanent dashboard navigation rail shell integration boundary carries shell read model", () => {
  const boundary = buildPermanentDashboardNavigationRailShellIntegrationBoundary({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(boundary.shellReadModel.activeSurfaceId, "engineering_3d_cad_cam");
  assert.equal(boundary.shellReadModel.density, "expanded");
  assert.equal(boundary.shellReadModel.totalSections, 19);
  assert.equal(boundary.shellReadModel.totalItems, 38);
  assert.equal(boundary.shellReadModel.selectedItems, 1);
  assert.equal(boundary.shellReadModel.threeDItems, 1);
  assert.equal(boundary.shellReadModel.simulationItems, 4);
});
