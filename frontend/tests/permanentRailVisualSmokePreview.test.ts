import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentRailVisualSmokePreview,
  validatePermanentRailVisualSmokePreview,
} from "../react_flow_preview/src/permanentRailVisualSmokePreview.js";

test("permanent rail visual smoke preview validates cleanly", () => {
  const validation = validatePermanentRailVisualSmokePreview();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent rail visual smoke preview exposes component and canonical counts", () => {
  const preview = buildPermanentRailVisualSmokePreview();

  assert.equal(preview.componentExportName, "PermanentDashboardNavigationRail");
  assert.equal(preview.componentAvailable, true);
  assert.equal(preview.totalSections, 19);
  assert.equal(preview.totalItems, 38);
  assert.equal(preview.selectedItems, 1);
});

test("permanent rail visual smoke preview keeps compact rail by default", () => {
  const preview = buildPermanentRailVisualSmokePreview();

  assert.equal(preview.activeSurfaceId, "operator_home");
  assert.equal(preview.density, "compact");
  assert.equal(preview.railWidthPx, 104);
});

test("permanent rail visual smoke preview supports expanded 3d surface", () => {
  const preview = buildPermanentRailVisualSmokePreview({
    activeSurfaceId: "engineering_3d_cad_cam",
    density: "expanded",
  });

  assert.equal(preview.activeSurfaceId, "engineering_3d_cad_cam");
  assert.equal(preview.density, "expanded");
  assert.equal(preview.railWidthPx, 284);
  assert.equal(preview.shellReadModel.threeDItems, 1);
  assert.equal(preview.shellReadModel.simulationItems, 4);
});

test("permanent rail visual smoke preview preserves layout separation", () => {
  const preview = buildPermanentRailVisualSmokePreview();

  assert.equal(preview.railBeforeCenterViewport, true);
  assert.equal(preview.railPersistent, true);
  assert.equal(preview.railOverlay, false);
  assert.equal(preview.railDrawer, false);
  assert.equal(preview.centerViewportUsesRemainingWidth, true);
  assert.equal(preview.contextualDrawersActiveDashboardOnly, true);
  assert.equal(preview.topChatSeparate, true);
});

test("permanent rail visual smoke preview forbids manual recreation", () => {
  const preview = buildPermanentRailVisualSmokePreview();

  assert.equal(preview.manualDashboardButtonListAllowed, false);
  assert.equal(preview.manualRendererRouteLogicAllowed, false);
  assert.equal(preview.manualTaxonomyDuplicationAllowed, false);
});
