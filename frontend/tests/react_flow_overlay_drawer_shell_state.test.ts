import test from "node:test";
import assert from "node:assert/strict";
import {
  buildInitialOverlayDrawerShellState,
  toggleOverlayDrawerMode,
} from "../react_flow_preview/src/overlayDrawerShellState.js";

test("overlay drawer shell state starts hidden and chat-first on top", () => {
  const state = buildInitialOverlayDrawerShellState();

  assert.equal(state.leftMode, "hidden");
  assert.equal(state.rightMode, "hidden");
  assert.equal(state.topMode, "hidden");
  assert.equal(state.activeTopSection, "jarvis_chat");
});

test("toggle overlay drawer mode switches hidden and expanded", () => {
  assert.equal(toggleOverlayDrawerMode("hidden"), "expanded");
  assert.equal(toggleOverlayDrawerMode("expanded"), "hidden");
});
