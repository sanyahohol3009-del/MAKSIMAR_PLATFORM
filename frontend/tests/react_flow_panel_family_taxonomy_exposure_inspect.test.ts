import test from "node:test";
import assert from "node:assert/strict";
import { buildPanelFamilyTaxonomyExposureInspectPresentation } from "../react_flow_preview/src/panelFamilyTaxonomyExposureInspect.js";

test("panel family/taxonomy/exposure inspect builds foundation entry", () => {
  const inspect = buildPanelFamilyTaxonomyExposureInspectPresentation(
    "system_status",
  );

  assert.equal(inspect.title, "System Status");
  assert.equal(inspect.semanticKind, "panel_family_taxonomy_exposure");
  assert.equal(inspect.sections.length, 2);
  assert.equal(inspect.sections[0]?.items.length, 4);
});

test("panel family/taxonomy/exposure inspect builds interaction entry", () => {
  const inspect = buildPanelFamilyTaxonomyExposureInspectPresentation(
    "approval_queue",
  );

  assert.equal(inspect.title, "Approval Queue");
  assert.equal(inspect.sections[1]?.items[1]?.value, "policy_visible");
});
