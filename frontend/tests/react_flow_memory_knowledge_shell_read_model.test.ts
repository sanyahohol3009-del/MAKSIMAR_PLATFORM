import test from "node:test";
import assert from "node:assert/strict";
import { buildMemoryKnowledgeShellReadModel } from "../react_flow_preview/src/memoryKnowledgeShellReadModel.js";

test("memory/knowledge shell read model builds inspect exposure", () => {
  const model = buildMemoryKnowledgeShellReadModel("memory_registry_summary");
  assert.equal(model.activeEntry.targetSurface, "inspect");
  assert.equal(model.snapshot.totalEntries, 4);
});

test("memory/knowledge shell read model builds chat context exposure", () => {
  const model = buildMemoryKnowledgeShellReadModel("project_context_summary");
  assert.equal(model.activeEntry.targetSurface, "chat_context");
  assert.equal(model.activeInspect.title, "Project Context Summary");
  assert.equal(model.activeInspect.sections.length, 2);
});
