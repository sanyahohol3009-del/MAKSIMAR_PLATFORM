import test from "node:test";
import assert from "node:assert/strict";

import { buildExplainPanelContract } from "../contracts/explain_panel_contract.js";

test("explain panel contract builds", () => {
  const contract = buildExplainPanelContract();
  assert.equal(contract.explainPanelId, "explain_panel_contract_001");
  assert.equal(contract.preferredZone, "zone_explainability");
});
