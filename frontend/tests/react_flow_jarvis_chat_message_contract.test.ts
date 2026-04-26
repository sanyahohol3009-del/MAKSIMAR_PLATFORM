import test from "node:test";
import assert from "node:assert/strict";
import { buildJarvisChatMessageContract } from "../react_flow_preview/src/jarvis_chat/jarvisChatMessageContract.js";

test("jarvis chat message contract builds text message", () => {
  const message = buildJarvisChatMessageContract({
    messageId: "msg_test_text",
    role: "user",
    kind: "text",
    createdAt: "2026-04-26T18:10:00Z",
    body: "Hello JARVIS",
    sourceScope: "chat",
  });

  assert.equal(message.role, "user");
  assert.equal(message.kind, "text");
  assert.equal(message.language, null);
  assert.equal(message.isExecutable, false);
});

test("jarvis chat message contract builds copyable code block", () => {
  const message = buildJarvisChatMessageContract({
    messageId: "msg_test_code",
    role: "jarvis",
    kind: "code",
    createdAt: "2026-04-26T18:10:10Z",
    body: "print('hello')",
    language: "python",
    sourceScope: "chat",
  });

  assert.equal(message.kind, "code");
  assert.equal(message.language, "python");
  assert.equal(message.isExecutable, false);
  assert.equal(message.isGuarded, true);
});
