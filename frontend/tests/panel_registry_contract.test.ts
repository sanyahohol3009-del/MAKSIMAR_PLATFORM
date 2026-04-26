import test from "node:test";
import assert from "node:assert/strict";

import { buildPanelRegistryContract } from "../contracts/panel_registry_contract.js";

test("panel registry contract builds", () => {
  const contract = buildPanelRegistryContract();
  assert.equal(contract.registryId, "panel_registry_contract_001");
  assert.equal(contract.entries.length, 4);
});
