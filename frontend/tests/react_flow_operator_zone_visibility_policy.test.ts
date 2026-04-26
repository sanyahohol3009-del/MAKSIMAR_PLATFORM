import test from "node:test";
import assert from "node:assert/strict";
import { buildOperatorZoneVisibilityPolicy } from "../react_flow_preview/src/operator_shell/operatorZoneVisibilityPolicy.js";

test("operator zone visibility policy sets fullscreen communication mode correctly", () => {
  const policy = buildOperatorZoneVisibilityPolicy("communication_focus");

  assert.equal(policy.length, 5);
  assert.equal(policy[0]?.zoneId, "top_communication");
  assert.equal(policy[0]?.visibilityState, "fullscreen_overlay");
  assert.equal(policy[1]?.visibilityState, "hidden");
  assert.equal(policy[2]?.visibilityState, "hidden");
});

test("operator zone visibility policy keeps center and footer always visible in baseline", () => {
  const policy = buildOperatorZoneVisibilityPolicy("baseline");

  const center = policy.find((row) => row.zoneId === "center_scene");
  const footer = policy.find((row) => row.zoneId === "bottom_footer");

  assert.equal(center?.visibilityState, "always_visible");
  assert.equal(footer?.visibilityState, "always_visible");
  assert.equal(center?.centerImmutable, true);
  assert.equal(footer?.centerImmutable, true);
});
