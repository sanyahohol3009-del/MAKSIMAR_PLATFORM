import assert from "node:assert/strict";
import test from "node:test";

import {
  ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX,
  CENTER_VIEWPORT_LEFT_OFFSET_PX,
  LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX,
  PERMANENT_RAIL_COMPACT_WIDTH_PX,
  PERMANENT_RAIL_EXPANDED_WIDTH_PX,
  VISIBLE_PERMANENT_RAIL_WIDTH_PX,
  buildAppShellPermanentRailLayoutOffsetsReadModel,
  validateAppShellPermanentRailLayoutOffsetsReadModel,
} from "../react_flow_preview/src/appShellPermanentRailLayoutOffsets.js";

test("AppShell permanent rail layout offsets validate cleanly", () => {
  const validation = validateAppShellPermanentRailLayoutOffsetsReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("AppShell permanent rail layout offsets preserve compact and expanded widths", () => {
  assert.equal(PERMANENT_RAIL_COMPACT_WIDTH_PX, 104);
  assert.equal(PERMANENT_RAIL_EXPANDED_WIDTH_PX, 284);
  assert.equal(VISIBLE_PERMANENT_RAIL_WIDTH_PX, 284);
});

test("AppShell permanent rail layout offsets separate rail, center and active drawer", () => {
  assert.equal(CENTER_VIEWPORT_LEFT_OFFSET_PX, VISIBLE_PERMANENT_RAIL_WIDTH_PX);
  assert.equal(
    ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX,
    VISIBLE_PERMANENT_RAIL_WIDTH_PX,
  );
  assert.equal(
    LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX,
    VISIBLE_PERMANENT_RAIL_WIDTH_PX,
  );
});

test("AppShell permanent rail layout offsets expose semantic read model", () => {
  const readModel = buildAppShellPermanentRailLayoutOffsetsReadModel();

  assert.equal(readModel.target, "appshell_permanent_rail_layout_offsets");
  assert.equal(readModel.visiblePermanentRailWidthPx, 284);
  assert.equal(readModel.centerViewportLeftOffsetPx, 284);
  assert.equal(readModel.activeDashboardLeftDrawerLeftOffsetPx, 284);
  assert.equal(readModel.leftDrawerHandleLeftOffsetPx, 284);
  assert.equal(readModel.permanentRailIsDashboardSelector, true);
  assert.equal(readModel.activeLeftDrawerIsDashboardContext, true);
});
