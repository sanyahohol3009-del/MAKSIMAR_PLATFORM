import test from "node:test";
import assert from "node:assert/strict";
import {
  buildTopCommunicationDensityReadModel,
  resolveTopCommunicationDensityMode,
} from "../react_flow_preview/src/operator_shell/topCommunicationDensityReadModel.js";

test("top communication density read model resolves normalized mode for fullscreen communication", () => {
  const mode = resolveTopCommunicationDensityMode({
    fullscreenCommunication: true,
  });

  assert.equal(mode, "normalized_density");
});

test("top communication density read model confirms dominant content in normalized mode", () => {
  const model = buildTopCommunicationDensityReadModel({
    fullscreenCommunication: true,
  });

  assert.equal(model.mode, "normalized_density");
  assert.equal(model.contentDominant, true);
  assert.equal(model.hiddenBlocks, 1);
  assert.equal(model.collapsedBlocks, 2);
  assert.equal(model.dominantBlocks, 1);
});
