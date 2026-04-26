import test from "node:test";
import assert from "node:assert/strict";
import { buildEmbeddedChatSurfaceInspectPresentation } from "../react_flow_preview/src/jarvis_chat/embeddedChatSurfaceInspect.js";

test("embedded chat surface inspect builds project-context host presentation", () => {
  const inspect = buildEmbeddedChatSurfaceInspectPresentation(
    "project_context_host",
  );

  assert.equal(inspect.title, "Project Context Host");
  assert.equal(inspect.semanticKind, "embedded_chat_surface");
  assert.equal(inspect.sections.length, 2);
  assert.equal(inspect.sections[0]?.items[0]?.value, "project_context_host");
});

test("embedded chat surface inspect keeps code output copyable and non-executing", () => {
  const inspect = buildEmbeddedChatSurfaceInspectPresentation(
    "code_output_lane",
  );

  const safetySection = inspect.sections[1];
  assert.equal(safetySection?.title, "Code Output Safety");
  assert.equal(safetySection?.items[1]?.value, "true");
  assert.equal(safetySection?.items[2]?.value, "true");
});
