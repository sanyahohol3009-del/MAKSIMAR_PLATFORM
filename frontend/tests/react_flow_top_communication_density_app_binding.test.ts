import test from "node:test";
import assert from "node:assert/strict";
import { buildTopCommunicationDensityAppBinding } from "../react_flow_preview/src/operator_shell/topCommunicationDensityAppBinding.js";

test("top communication density app binding collapses selector and chips in normalized mode", () => {
  const binding = buildTopCommunicationDensityAppBinding({
    fullscreenCommunication: true,
  });

  assert.equal(binding.mode, "normalized_density");
  assert.equal(binding.showSectionTabs, true);
  assert.equal(binding.showSurfaceSelector, true);
  assert.equal(binding.collapseSurfaceSelector, true);
  assert.equal(binding.showSummaryChipLane, true);
  assert.equal(binding.collapseSummaryChipLane, true);
  assert.equal(binding.showSupportMeta, false);
  assert.equal(binding.contentDominant, true);
});

test("top communication density app binding keeps baseline visibility in non-fullscreen mode", () => {
  const binding = buildTopCommunicationDensityAppBinding({
    fullscreenCommunication: false,
  });

  assert.equal(binding.mode, "baseline_density");
  assert.equal(binding.showSectionTabs, true);
  assert.equal(binding.showSurfaceSelector, true);
  assert.equal(binding.collapseSurfaceSelector, false);
  assert.equal(binding.showSummaryChipLane, true);
  assert.equal(binding.collapseSummaryChipLane, false);
  assert.equal(binding.showSupportMeta, true);
  assert.equal(binding.contentDominant, false);
});
