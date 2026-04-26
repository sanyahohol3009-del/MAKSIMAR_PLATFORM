import test from "node:test";
import assert from "node:assert/strict";
import {
  getMemoryKnowledgeExposureEntry,
  getMemoryKnowledgeExposureGroups,
  getMemoryKnowledgeExposureOrder,
  memoryKnowledgeExposureRegistry,
} from "../react_flow_preview/src/memoryKnowledgeExposureRegistry.js";

test("memory/knowledge exposure registry exposes stable order", () => {
  assert.deepEqual(getMemoryKnowledgeExposureOrder(), [
    "memory_registry_summary",
    "knowledge_registry_summary",
    "project_context_summary",
    "memory_policy_summary",
  ]);
});

test("memory/knowledge exposure registry contains four entries", () => {
  assert.equal(memoryKnowledgeExposureRegistry.length, 4);
});

test("memory/knowledge exposure groups preserve target surfaces", () => {
  const groups = getMemoryKnowledgeExposureGroups();
  assert.deepEqual(
    groups.map((group) => group.targetSurface),
    ["inspect", "explain", "chat_context"],
  );
});

test("memory policy exposure resolves explain surface entry", () => {
  const entry = getMemoryKnowledgeExposureEntry("memory_policy_summary");
  assert.equal(entry.targetSurface, "explain");
  assert.equal(entry.canonicalOwner, "memory_policy_layer");
});
