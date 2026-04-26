import test from "node:test";
import assert from "node:assert/strict";
import { buildTopCommunicationDensityInspectPresentation } from "../react_flow_preview/src/operator_shell/topCommunicationDensityInspect.js";

test("top communication density inspect builds normalized presentation", () => {
  const inspect = buildTopCommunicationDensityInspectPresentation({
    fullscreenCommunication: true,
  });

  assert.equal(inspect.title, "Top Communication Density");
  assert.equal(inspect.subtitle, "normalized_density");
  assert.equal(inspect.semanticKind, "top_communication_density");
  assert.equal(inspect.sections.length, 3);
});

test("top communication density inspect exposes dominant content flag", () => {
  const inspect = buildTopCommunicationDensityInspectPresentation({
    fullscreenCommunication: true,
  });

  assert.equal(inspect.sections[0]?.items[1]?.value, "true");
  assert.equal(inspect.sections[1]?.items[1]?.value, "1");
});
