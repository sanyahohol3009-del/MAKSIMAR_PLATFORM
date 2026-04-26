import test from "node:test";
import assert from "node:assert/strict";
import { buildPanelNavigationReadModel } from "../react_flow_preview/src/panelNavigationReadModel.js";

test("panel navigation read model aggregates foundation and interaction counts", () => {
  const model = buildPanelNavigationReadModel();

  assert.equal(model.totalPanels, 8);
  assert.equal(model.foundationPanels, 5);
  assert.equal(model.interactionPanels, 3);
});

test("panel navigation read model preserves grouped navigation rows", () => {
  const model = buildPanelNavigationReadModel();

  assert.equal(model.groupedNavigation.length, 3);
  assert.equal(model.groupedNavigation[0]?.rows.length, 3);
  assert.equal(model.groupedNavigation[1]?.rows.length, 2);
  assert.equal(model.groupedNavigation[2]?.rows.length, 3);
});

test("panel navigation read model keeps workspace landing for foundation panels", () => {
  const model = buildPanelNavigationReadModel();
  const foundationRow = model.groupedNavigation[0]?.rows[0];

  assert.equal(
    foundationRow?.shellLanding,
    "main_operator_secondary_foundation_reuse",
  );
  assert.equal(
    foundationRow?.workspaceRole,
    "foundation_monitoring",
  );
});
