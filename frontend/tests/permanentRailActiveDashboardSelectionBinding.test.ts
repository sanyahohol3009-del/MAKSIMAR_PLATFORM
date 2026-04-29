import assert from "node:assert/strict";
import test from "node:test";

import {
  buildPermanentRailActiveDashboardSelectionBindingReadModel,
  getActiveViewForPermanentRailSurfaceId,
  getPermanentRailSelectionRouteBySurfaceId,
  validatePermanentRailActiveDashboardSelectionBindingReadModel,
} from "../react_flow_preview/src/permanentRailActiveDashboardSelectionBinding.js";

test("permanent rail active dashboard selection binding validates cleanly", () => {
  const validation = validatePermanentRailActiveDashboardSelectionBindingReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("permanent rail active dashboard selection binding exposes all dashboard routes", () => {
  const readModel = buildPermanentRailActiveDashboardSelectionBindingReadModel();

  assert.equal(readModel.target, "permanent_rail_active_dashboard_selection_binding");
  assert.equal(readModel.source, "dashboard_skeleton_navigation_renderer_route_binding");
  assert.equal(readModel.totalRoutes, 38);
  assert.equal(readModel.defaultSurfaceId, "operator_home");
  assert.equal(readModel.appTsxHardcodingAllowed, false);
  assert.equal(readModel.manualDashboardButtonListAllowed, false);
  assert.equal(readModel.manualRendererRouteLogicAllowed, false);
});

test("permanent rail active dashboard selection binding has at least one center-ready route", () => {
  const readModel = buildPermanentRailActiveDashboardSelectionBindingReadModel();

  if (readModel.centerViewportReadyRoutes < 1) {
    throw new Error("expected at least one center viewport ready route");
  }

  const readyRoute = readModel.routes.find(
    (route) => route.routeStatus === "center_viewport_ready",
  );

  if (!readyRoute) {
    throw new Error("expected ready route");
  }

  assert.equal(
    getActiveViewForPermanentRailSurfaceId(readyRoute.surfaceId),
    readyRoute.activeView,
  );
});

test("permanent rail active dashboard selection binding resolves operator home route", () => {
  const route = getPermanentRailSelectionRouteBySurfaceId("operator_home");

  if (!route) {
    throw new Error("expected operator_home route");
  }

  assert.equal(route.surfaceId, "operator_home");
  assert.equal(route.appTsxHardcodingAllowed, false);
});

test("permanent rail active dashboard selection binding returns null for missing surface", () => {
  assert.equal(getPermanentRailSelectionRouteBySurfaceId("missing_surface"), null);
  assert.equal(getActiveViewForPermanentRailSurfaceId("missing_surface"), null);
});
