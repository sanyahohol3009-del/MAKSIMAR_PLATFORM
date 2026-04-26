import test from "node:test";
import assert from "node:assert/strict";
import { buildJarvisChatDrawerFixture } from "../react_flow_preview/src/jarvis_chat/jarvisChatDrawerFixture.js";

test("jarvis chat session contract is overlay-only and project-aware", () => {
  const fixture = buildJarvisChatDrawerFixture();
  const session = fixture.session;

  assert.equal(session.drawerId, "top_chat_drawer");
  assert.equal(session.isOverlayOnly, true);
  assert.equal(session.isUndockable, true);
  assert.equal(session.hasProjectContext, true);
});

test("jarvis chat session contract preserves command support and diagnostics", () => {
  const fixture = buildJarvisChatDrawerFixture();
  const session = fixture.session;

  assert.equal(session.hasCommandSupport, true);
  assert.equal(session.hasDiagnosticsSummary, true);
  assert.equal(session.defaultVisibility, "hidden");
  assert.equal(session.unreadCount, 2);
});
