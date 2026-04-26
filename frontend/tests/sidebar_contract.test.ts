import test from "node:test";
import assert from "node:assert/strict";

import { buildSidebarContract } from "../contracts/sidebar_contract.js";

test("sidebar contract builds", () => {
  const contract = buildSidebarContract();
  assert.equal(contract.sidebarId, "sidebar_contract_001");
  assert.equal(contract.items.length, 3);
});
