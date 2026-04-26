import test from "node:test";
import assert from "node:assert/strict";
import { buildOperatorZoneAppBinding } from "../react_flow_preview/src/operator_shell/operatorZoneAppBinding.js";

test("operator zone app binding hides side drawers during communication focus", () => {
  const binding = buildOperatorZoneAppBinding({
    topMode: "expanded",
    leftMode: "expanded",
    rightMode: "expanded",
  });

  assert.equal(binding.shellMode, "communication_focus");
  assert.equal(binding.showTopCommunicationOverlay, true);
  assert.equal(binding.showLeftDrawer, false);
  assert.equal(binding.showRightDrawer, false);
  assert.equal(binding.showLeftHandle, false);
  assert.equal(binding.showRightHandle, false);
  assert.equal(binding.showSummaryCards, false);
});

test("operator zone app binding keeps left drawer visible in left-navigation focus", () => {
  const binding = buildOperatorZoneAppBinding({
    topMode: "hidden",
    leftMode: "expanded",
    rightMode: "hidden",
  });

  assert.equal(binding.shellMode, "left_navigation_focus");
  assert.equal(binding.showLeftDrawer, true);
  assert.equal(binding.showRightDrawer, false);
  assert.equal(binding.showTopCommunicationOverlay, false);
  assert.equal(binding.showFooter, true);
});

test("operator zone app binding keeps summary cards only in baseline mode", () => {
  const binding = buildOperatorZoneAppBinding({
    topMode: "hidden",
    leftMode: "hidden",
    rightMode: "hidden",
  });

  assert.equal(binding.shellMode, "baseline");
  assert.equal(binding.showSummaryCards, true);
  assert.equal(binding.centerImmutableConfirmed, true);
});
