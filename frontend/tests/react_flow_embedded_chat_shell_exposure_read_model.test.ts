import test from "node:test";
import assert from "node:assert/strict";
import { buildEmbeddedChatShellExposureReadModel } from "../react_flow_preview/src/jarvis_chat/embeddedChatShellExposureReadModel.js";

test("embedded chat shell exposure read model aggregates primary and reference rows", () => {
  const model = buildEmbeddedChatShellExposureReadModel();

  assert.equal(model.primaryTopDrawerRows, 4);
  assert.equal(model.leftReferenceRows, 1);
  assert.equal(model.rightReferenceRows, 1);
  assert.equal(model.totalSurfaceRows, 6);
});

test("embedded chat shell exposure read model keeps duplication control enabled", () => {
  const model = buildEmbeddedChatShellExposureReadModel();

  assert.equal(model.projectContextBindingReady, true);
  assert.equal(model.duplicationControlEnabled, true);
  assert.equal(model.groupedExposure.length, 3);
  assert.equal(model.groupedExposure[0]?.target, "top_drawer_primary");
  assert.equal(model.groupedExposure[1]?.target, "left_drawer_context_reference");
  assert.equal(model.groupedExposure[2]?.target, "right_drawer_inspect_reference");
});
