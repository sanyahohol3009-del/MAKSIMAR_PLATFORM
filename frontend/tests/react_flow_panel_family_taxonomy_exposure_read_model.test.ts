import test from "node:test";
import assert from "node:assert/strict";
import { buildPanelFamilyTaxonomyExposureReadModel } from "../react_flow_preview/src/panelFamilyTaxonomyExposureReadModel.js";

test("panel family/taxonomy read model aggregates family and visibility counts", () => {
  const model = buildPanelFamilyTaxonomyExposureReadModel();

  assert.equal(model.totalPanels, 8);
  assert.equal(model.foundationPanels, 5);
  assert.equal(model.interactionPanels, 3);
  assert.equal(model.alwaysVisiblePanels, 5);
  assert.equal(model.policyVisiblePanels, 3);
});

test("panel family/taxonomy read model preserves grouped taxonomy rows", () => {
  const model = buildPanelFamilyTaxonomyExposureReadModel();

  assert.equal(model.groupedTaxonomy.length, 3);
  assert.equal(model.groupedTaxonomy[0]?.rows.length, 3);
  assert.equal(model.groupedTaxonomy[1]?.rows.length, 2);
  assert.equal(model.groupedTaxonomy[2]?.rows.length, 3);
});
