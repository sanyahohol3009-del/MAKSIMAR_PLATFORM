import test from "node:test";
import assert from "node:assert/strict";
import {
  buildMemoryKnowledgeExposureSnapshot,
  buildMemoryKnowledgeInspectPresentation,
} from "../react_flow_preview/src/memoryKnowledgeExposureSemantics.js";

test("memory/knowledge snapshot aggregates grouped exposure counts", () => {
  const snapshot = buildMemoryKnowledgeExposureSnapshot();
  assert.equal(snapshot.totalEntries, 4);
  assert.equal(snapshot.inspectEntries, 2);
  assert.equal(snapshot.explainEntries, 1);
  assert.equal(snapshot.chatContextEntries, 1);
});

test("memory/knowledge inspect presentation builds project context entry", () => {
  const inspect = buildMemoryKnowledgeInspectPresentation(
    "project_context_summary",
  );
  assert.equal(inspect.title, "Project Context Summary");
  assert.equal(inspect.semanticKind, "chat_context_memory_knowledge_exposure");
  assert.equal(inspect.sections.length, 2);
  assert.equal(inspect.sections[0]?.items.length, 2);
});
