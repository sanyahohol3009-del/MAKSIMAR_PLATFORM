import test from "node:test";
import assert from "node:assert/strict";
import { buildEmbeddedChatSurfaceReadModel } from "../react_flow_preview/src/jarvis_chat/embeddedChatSurfaceReadModel.js";

test("embedded chat surface read model aggregates canonical counts", () => {
  const model = buildEmbeddedChatSurfaceReadModel();

  assert.equal(model.totalSurfaces, 4);
  assert.equal(model.totalHistoryMessages, 6);
  assert.equal(model.totalCodeBlocks, 1);
  assert.equal(model.totalCommandSupportUnits, 3);
  assert.equal(model.copyableCodeBlocks, 1);
});

test("embedded chat surface read model confirms project-context binding readiness", () => {
  const model = buildEmbeddedChatSurfaceReadModel();

  assert.equal(model.projectContextBindingReady, true);
  assert.equal(model.groupedRows.length, 4);
  assert.equal(model.groupedRows[0]?.shellLane, "communication");
  assert.equal(model.groupedRows[1]?.shellLane, "history");
  assert.equal(model.groupedRows[2]?.shellLane, "output");
  assert.equal(model.groupedRows[3]?.shellLane, "support");
});
