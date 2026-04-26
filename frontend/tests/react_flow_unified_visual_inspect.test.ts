import test from "node:test";
import assert from "node:assert/strict";
import { buildUnifiedVisualInspectPresentation } from "../react_flow_preview/src/unifiedVisualInspectSemantics.js";

test("unified visual inspect builds default graph inspect presentation", () => {
  const inspect = buildUnifiedVisualInspectPresentation("graph:topology", null);
  assert.equal(inspect.title.length > 0, true);
  assert.equal(inspect.semanticKind.length > 0, true);
  assert.equal(inspect.sections.length > 0, true);
});

test("unified visual inspect builds chart inspect presentation", () => {
  const inspect = buildUnifiedVisualInspectPresentation(
    "chart:node_resources",
    null,
  );
  assert.equal(inspect.title, "Node Resources");
  assert.equal(inspect.semanticKind, "bar_telemetry_chart");
  assert.equal(inspect.sections.length, 1);
  assert.equal(inspect.sections[0]?.items.length, 4);
});
