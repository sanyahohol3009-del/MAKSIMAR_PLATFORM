import assert from "node:assert/strict";
import test from "node:test";

import {
  SUMMARY_CARDS_LEFT_OFFSET_PX,
  VISIBLE_PERMANENT_RAIL_WIDTH_PX,
  buildAppShellPermanentRailLayoutOffsetsReadModel,
  validateAppShellPermanentRailLayoutOffsetsReadModel,
} from "../react_flow_preview/src/appShellPermanentRailLayoutOffsets.js";

test("AppShell permanent rail cosmetic offsets validate cleanly", () => {
  const validation = validateAppShellPermanentRailLayoutOffsetsReadModel();

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("AppShell permanent rail cosmetic offsets move summary cards after rail", () => {
  assert.equal(SUMMARY_CARDS_LEFT_OFFSET_PX, VISIBLE_PERMANENT_RAIL_WIDTH_PX);
  assert.equal(SUMMARY_CARDS_LEFT_OFFSET_PX, 284);
});

test("AppShell permanent rail cosmetic offsets preserve dashboard/context separation", () => {
  const readModel = buildAppShellPermanentRailLayoutOffsetsReadModel();

  assert.equal(readModel.permanentRailIsDashboardSelector, true);
  assert.equal(readModel.activeLeftDrawerIsDashboardContext, true);
  assert.equal(readModel.summaryCardsLeftOffsetPx, 284);
});
