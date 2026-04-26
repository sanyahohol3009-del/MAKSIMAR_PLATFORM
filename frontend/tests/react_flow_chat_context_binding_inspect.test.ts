import test from "node:test";
import assert from "node:assert/strict";
import {
  buildChatContextBindingInspectPresentation,
  getChatContextBindingDisplayTitle,
} from "../react_flow_preview/src/chatContextBindingInspect.js";

test("chat context binding display title resolves project context host binding", () => {
  assert.equal(
    getChatContextBindingDisplayTitle(
      "project_context_to_embedded_chat_host",
    ),
    "Project Context → Embedded Chat Host",
  );
});

test("chat context binding inspect builds project context entry", () => {
  const inspect = buildChatContextBindingInspectPresentation(
    "project_context_to_embedded_chat_host",
  );

  assert.equal(inspect.semanticKind, "embedded_chat_context_binding");
  assert.equal(inspect.sections.length, 2);
  assert.equal(inspect.sections[0]?.items.length, 4);
  assert.equal(inspect.sections[1]?.items[3]?.value, "false");
});

test("chat context binding inspect builds command strip support entry", () => {
  const inspect = buildChatContextBindingInspectPresentation(
    "command_strip_chat_support_binding",
  );

  assert.equal(inspect.title, "Command Strip → Chat Support");
  assert.equal(inspect.sections[1]?.items[5]?.value, "true");
});
