import test from "node:test";
import assert from "node:assert/strict";
import { buildJarvisChatDrawerContract } from "../react_flow_preview/src/jarvis_chat/jarvisChatDrawerContract.js";

test("jarvis chat drawer contract remains top overlay and preserves center canvas", () => {
  const contract = buildJarvisChatDrawerContract();

  assert.equal(contract.edge, "top");
  assert.equal(contract.overlayOnly, true);
  assert.equal(contract.defaultState, "hidden");
  assert.equal(contract.preservesCenterCanvas, true);
  assert.equal(contract.glassOverlay, true);
});

test("jarvis chat drawer contract remains chat-first with collapsed strip label", () => {
  const contract = buildJarvisChatDrawerContract();

  assert.equal(contract.primarySurface, "jarvis_chat");
  assert.equal(contract.collapsedStripLabel.length > 0, true);
  assert.equal(contract.projectTitleStripVisibleWhenHidden, true);
  assert.deepEqual(contract.sections, [
    "conversation",
    "project_context",
    "command_handoff",
    "diagnostics",
  ]);
});
