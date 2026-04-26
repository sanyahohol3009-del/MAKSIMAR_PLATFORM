import test from "node:test";
import assert from "node:assert/strict";
import { buildOperatorZoneVisibilityInspectPresentation } from "../react_flow_preview/src/operator_shell/operatorZoneVisibilityInspect.js";

test("operator zone visibility inspect builds communication focus presentation", () => {
  const inspect = buildOperatorZoneVisibilityInspectPresentation({
    topMode: "expanded",
    leftMode: "hidden",
    rightMode: "hidden",
  });

  assert.equal(inspect.title, "Operator Zone Visibility");
  assert.equal(inspect.subtitle, "communication_focus");
  assert.equal(inspect.semanticKind, "operator_zone_visibility");
  assert.equal(inspect.sections.length, 3);
});

test("operator zone visibility inspect exposes fullscreen communication flag", () => {
  const inspect = buildOperatorZoneVisibilityInspectPresentation({
    topMode: "expanded",
    leftMode: "hidden",
    rightMode: "hidden",
  });

  assert.equal(inspect.sections[0]?.items[1]?.value, "true");
  assert.equal(inspect.sections[1]?.items[0]?.value, "5");
});
