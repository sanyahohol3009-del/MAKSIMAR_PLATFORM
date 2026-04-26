import test from "node:test";
import assert from "node:assert/strict";
import { buildOverlayDrawerLayoutContract } from "../react_flow_preview/src/overlayDrawerLayoutContract.js";

test("overlay drawer layout contract keeps center canvas immutable", () => {
  const contract = buildOverlayDrawerLayoutContract();

  assert.equal(contract.centerCanvasPolicy, "persistent_fullscreen_canvas");
  assert.equal(contract.centerCanvasAlwaysVisible, true);
  assert.equal(contract.centerCanvasMovesOnDrawerOpen, false);
  assert.equal(contract.centerCanvasResizesOnDrawerOpen, false);
  assert.equal(contract.centerCanvasIsPrimaryVisualSurface, true);
});

test("all drawers are hidden by default and overlay-only", () => {
  const contract = buildOverlayDrawerLayoutContract();
  const drawers = [
    contract.drawers.left,
    contract.drawers.right,
    contract.drawers.top,
  ];

  assert.equal(drawers.every((drawer) => drawer.defaultMode === "hidden"), true);
  assert.equal(
    drawers.every(
      (drawer) =>
        drawer.pushesCenterCanvas === false &&
        drawer.resizesCenterCanvas === false &&
        drawer.blocksCenterCanvasLayout === false,
    ),
    true,
  );
});

test("top drawer defaults to jarvis chat and remains glass overlay", () => {
  const contract = buildOverlayDrawerLayoutContract();

  assert.equal(contract.drawers.top.activeSection, "jarvis_chat");
  assert.equal(contract.drawers.top.visualStyle, "glass_overlay");
  assert.equal(contract.drawers.top.opensOnHandleClick, true);
  assert.equal(contract.drawers.top.closesOnHandleClick, true);
});

test("left drawer contains navigation and embedded chat context sections", () => {
  const contract = buildOverlayDrawerLayoutContract();

  assert.deepEqual(contract.drawers.left.availableSections, [
    "visual_registry_navigation",
    "panel_navigation",
    "embedded_chat_context",
  ]);
});
