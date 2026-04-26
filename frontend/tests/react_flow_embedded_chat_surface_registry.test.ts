import test from "node:test";
import assert from "node:assert/strict";
import {
  buildEmbeddedChatSurfaceRegistry,
  getEmbeddedChatSurfaceEntry,
} from "../react_flow_preview/src/jarvis_chat/embeddedChatSurfaceRegistry.js";

test("embedded chat surface registry exposes stable canonical order", () => {
  const registry = buildEmbeddedChatSurfaceRegistry();

  assert.deepEqual(
    registry.map((entry) => entry.surfaceId),
    [
      "project_context_host",
      "conversation_history_lane",
      "code_output_lane",
      "command_support_lane",
    ],
  );
});

test("embedded chat surface registry keeps code output copyable and non-executing", () => {
  const entry = getEmbeddedChatSurfaceEntry("code_output_lane");

  assert.equal(entry.copyable, true);
  assert.equal(entry.nonExecutable, true);
  assert.equal(entry.readOnly, true);
});
