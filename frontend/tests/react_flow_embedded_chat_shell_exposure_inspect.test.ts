import test from "node:test";
import assert from "node:assert/strict";
import { buildEmbeddedChatShellExposureInspectPresentation } from "../react_flow_preview/src/jarvis_chat/embeddedChatShellExposureInspect.js";

test("embedded chat shell exposure inspect builds project-context primary plus left reference", () => {
  const inspect = buildEmbeddedChatShellExposureInspectPresentation(
    "project_context_host",
  );

  assert.equal(inspect.title, "Project Context Host");
  assert.equal(inspect.semanticKind, "embedded_chat_shell_exposure");
  assert.equal(inspect.sections[0]?.items[1]?.value, "top_drawer_primary");
  assert.equal(
    inspect.sections[1]?.items[0]?.value,
    "embedded_chat_context / reference_only",
  );
});

test("embedded chat shell exposure inspect builds command-support primary plus right reference", () => {
  const inspect = buildEmbeddedChatShellExposureInspectPresentation(
    "command_support_lane",
  );

  assert.equal(inspect.title, "Command Support Lane");
  assert.equal(inspect.sections[0]?.items[2]?.value, "jarvis_chat_drawer");
  assert.equal(
    inspect.sections[1]?.items[0]?.value,
    "inspect / reference_only",
  );
});
