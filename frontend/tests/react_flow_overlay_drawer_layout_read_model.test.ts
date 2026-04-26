import test from "node:test";
import assert from "node:assert/strict";
import { buildOverlayDrawerLayoutReadModel } from "../react_flow_preview/src/overlayDrawerLayoutReadModel.js";

test("overlay drawer read model aggregates hidden and undockable drawers", () => {
  const model = buildOverlayDrawerLayoutReadModel();

  assert.equal(model.totalDrawers, 3);
  assert.equal(model.hiddenByDefaultCount, 3);
  assert.equal(model.undockCapableCount, 3);
});

test("overlay drawer read model preserves overlay-only center policy", () => {
  const model = buildOverlayDrawerLayoutReadModel();

  assert.equal(model.overlayOnly, true);
  assert.equal(model.centerCanvasAlwaysVisible, true);
  assert.equal(model.centerCanvasMovesOnDrawerOpen, false);
  assert.equal(model.centerCanvasResizesOnDrawerOpen, false);
});

test("overlay drawer read model keeps top drawer chat-first", () => {
  const model = buildOverlayDrawerLayoutReadModel();

  assert.equal(model.topDrawerDefaultsToChat, true);
  assert.equal(model.drawerSummaries[2]?.drawerId, "top");
  assert.equal(model.drawerSummaries[2]?.sections[0]?.sectionId, "jarvis_chat");
});
