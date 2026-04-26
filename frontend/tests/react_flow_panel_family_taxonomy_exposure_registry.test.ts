import test from "node:test";
import assert from "node:assert/strict";
import {
  getPanelFamilyTaxonomyExposureEntry,
  getPanelFamilyTaxonomyGroups,
  panelFamilyTaxonomyExposureRegistry,
} from "../react_flow_preview/src/panelFamilyTaxonomyExposureRegistry.js";

test("panel family/taxonomy/exposure registry contains eight panels", () => {
  assert.equal(panelFamilyTaxonomyExposureRegistry.length, 8);
});

test("panel family/taxonomy groups preserve shell taxonomy order", () => {
  const groups = getPanelFamilyTaxonomyGroups();

  assert.deepEqual(
    groups.map((group) => group.shellTaxonomy),
    [
      "foundation_status",
      "foundation_observability",
      "operator_interaction",
    ],
  );
});

test("topology entry resolves as foundation observability", () => {
  const entry = getPanelFamilyTaxonomyExposureEntry("topology");

  assert.equal(entry.panelFamily, "foundation");
  assert.equal(entry.shellTaxonomy, "foundation_observability");
  assert.equal(entry.visibilityPolicy, "always_visible");
});

test("approval queue entry resolves as policy-visible interaction", () => {
  const entry = getPanelFamilyTaxonomyExposureEntry("approval_queue");

  assert.equal(entry.panelFamily, "interaction");
  assert.equal(entry.shellTaxonomy, "operator_interaction");
  assert.equal(entry.visibilityPolicy, "policy_visible");
});
