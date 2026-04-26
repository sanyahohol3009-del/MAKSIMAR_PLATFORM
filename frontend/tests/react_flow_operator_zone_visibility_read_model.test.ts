import test from "node:test";
import assert from "node:assert/strict";
import {
  buildOperatorZoneVisibilityReadModel,
  resolveOperatorShellMode,
} from "../react_flow_preview/src/operator_shell/operatorZoneVisibilityReadModel.js";

test("operator zone visibility read model resolves communication focus from top expanded", () => {
  const shellMode = resolveOperatorShellMode({
    topMode: "expanded",
    leftMode: "hidden",
    rightMode: "hidden",
  });

  assert.equal(shellMode, "communication_focus");
});

test("operator zone visibility read model confirms fullscreen communication state", () => {
  const model = buildOperatorZoneVisibilityReadModel({
    topMode: "expanded",
    leftMode: "hidden",
    rightMode: "hidden",
  });

  assert.equal(model.shellMode, "communication_focus");
  assert.equal(model.fullscreenCommunicationActive, true);
  assert.equal(model.centerImmutableConfirmed, true);
  assert.equal(model.totalZones, 5);
});
