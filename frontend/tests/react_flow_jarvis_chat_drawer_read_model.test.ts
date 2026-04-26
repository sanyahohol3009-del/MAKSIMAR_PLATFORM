import test from "node:test";
import assert from "node:assert/strict";
import { buildJarvisChatDrawerReadModel } from "../react_flow_preview/src/jarvis_chat/jarvisChatDrawerReadModel.js";

test("jarvis chat drawer read model aggregates messages and handoffs", () => {
  const model = buildJarvisChatDrawerReadModel();

  assert.equal(model.totalMessages, 6);
  assert.equal(model.codeBlockCount, 1);
  assert.equal(model.copyableCodeCount, 1);
  assert.equal(model.handoffCount, 2);
  assert.equal(model.guardedHandoffCount, 2);
  assert.equal(model.unreadCount, 2);
});

test("jarvis chat drawer read model preserves hidden chat-first overlay behavior", () => {
  const model = buildJarvisChatDrawerReadModel();

  assert.equal(model.topDrawerHiddenByDefault, true);
  assert.equal(model.preservesCenterCanvas, true);
  assert.equal(model.overlayOnly, true);
  assert.equal(model.chatFirstOrdering, true);
});

test("jarvis chat drawer read model exposes project context and command support", () => {
  const model = buildJarvisChatDrawerReadModel();

  assert.equal(model.projectContextBindingReady, true);
  assert.equal(model.projectContextVisible, true);
  assert.equal(model.commandSupportVisible, true);
  assert.equal(model.diagnosticsVisible, true);
  assert.equal(model.groupedSections.length, 4);
  assert.equal(model.groupedSections[0]?.sectionId, "conversation");
});
