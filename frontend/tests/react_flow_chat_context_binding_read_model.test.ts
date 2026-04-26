import test from "node:test";
import assert from "node:assert/strict";
import { buildChatContextBindingReadModel } from "../react_flow_preview/src/chatContextBindingReadModel.js";

test("chat context binding read model aggregates host and command support counts", () => {
  const model = buildChatContextBindingReadModel();

  assert.equal(model.totalEntries, 4);
  assert.equal(model.hostEntries, 2);
  assert.equal(model.commandSupportEntries, 2);
  assert.equal(model.guardedEntries, 4);
});

test("chat context binding read model marks project context binding ready", () => {
  const model = buildChatContextBindingReadModel();

  assert.equal(model.projectContextBindingReady, true);
  assert.equal(model.groupedBindings.length, 2);
  assert.equal(model.groupedBindings[0]?.rows.length, 2);
  assert.equal(model.groupedBindings[1]?.rows.length, 2);
});
