import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentRailVisibleLayoutVerification,
  validatePermanentRailVisibleLayoutVerification,
} from "../react_flow_preview/src/permanentRailVisibleLayoutVerification.js";
import {
  buildAppShellPermanentRailVisibleWiringContract,
} from "../react_flow_preview/src/appShellPermanentRailVisibleWiringContract.js";

test("permanent rail visible layout verification validates cleanly", () => {
  const validation = validatePermanentRailVisibleLayoutVerification();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent rail visible layout verification keeps rail before center viewport", () => {
  const readModel = buildPermanentRailVisibleLayoutVerification();

  assert.equal(readModel.railBeforeCenterViewport, true);
  assert.equal(readModel.railPersistent, true);
  assert.equal(readModel.railOverlay, false);
  assert.equal(readModel.railDrawer, false);
  assert.equal(readModel.railMayOverlapCenterViewport, false);
  assert.equal(readModel.centerViewportUsesRemainingWidth, true);
});

test("permanent rail visible layout verification keeps contextual drawers dashboard-specific", () => {
  const readModel = buildPermanentRailVisibleLayoutVerification();

  assert.equal(readModel.contextualDrawersActiveDashboardOnly, true);
  assert.equal(readModel.contextualDrawersMayContainMainDashboardList, false);
});

test("permanent rail visible layout verification keeps top chat separate", () => {
  const readModel = buildPermanentRailVisibleLayoutVerification();

  assert.equal(readModel.topChatSeparate, true);
  assert.equal(readModel.topChatMayContainDashboardNavigation, false);
});

test("permanent rail visible layout verification forbids manual App.tsx recreation", () => {
  const readModel = buildPermanentRailVisibleLayoutVerification();

  assert.equal(readModel.appTsxMayOnlyWireShellSlot, true);
  assert.equal(readModel.manualDashboardButtonListAllowed, false);
  assert.equal(readModel.manualRendererRouteLogicAllowed, false);
  assert.equal(readModel.manualTaxonomyDuplicationAllowed, false);
});

test("permanent rail visible layout verification preserves expanded width contract", () => {
  const contract = buildAppShellPermanentRailVisibleWiringContract({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  const readModel = buildPermanentRailVisibleLayoutVerification(contract);

  assert.equal(readModel.contract.railSlot.widthPx, 284);
  assert.equal(
    readModel.contract.preview.contract.integrationBoundary.shellReadModel.activeSurfaceId,
    "engineering_3d_cad_cam",
  );
});
