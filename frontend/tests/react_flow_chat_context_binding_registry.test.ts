import test from "node:test";
import assert from "node:assert/strict";
import {
  getChatContextBindingEntry,
  getChatContextBindingGroups,
  getChatContextBindingOrder,
  chatContextBindingRegistry,
} from "../react_flow_preview/src/chatContextBindingRegistry.js";

test("chat context binding registry exposes stable canonical order", () => {
  assert.deepEqual(getChatContextBindingOrder(), [
    "project_context_to_embedded_chat_host",
    "chat_panel_host_contract_binding",
    "command_queue_chat_support_binding",
    "command_strip_chat_support_binding",
  ]);
});

test("chat context binding registry contains four entries", () => {
  assert.equal(chatContextBindingRegistry.length, 4);
});

test("chat context binding groups preserve host and command support split", () => {
  const groups = getChatContextBindingGroups();

  assert.deepEqual(
    groups.map((group) => group.group),
    ["chat_host", "command_support"],
  );

  assert.deepEqual(groups[0]?.entryIds, [
    "project_context_to_embedded_chat_host",
    "chat_panel_host_contract_binding",
  ]);

  assert.deepEqual(groups[1]?.entryIds, [
    "command_queue_chat_support_binding",
    "command_strip_chat_support_binding",
  ]);
});

test("project context binding remains guarded and non-executing", () => {
  const entry = getChatContextBindingEntry(
    "project_context_to_embedded_chat_host",
  );

  assert.equal(entry.bindingMode, "read_only_context_binding");
  assert.equal(entry.guarded, true);
  assert.equal(entry.directExecutionAllowed, false);
  assert.equal(entry.targetSurface, "embedded_chat_host");
});
