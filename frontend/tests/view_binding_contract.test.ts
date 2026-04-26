import test from "node:test";
import assert from "node:assert/strict";

import { buildViewBindingContract } from "../contracts/view_binding_contract.js";

test("view binding contract builds", () => {
  const contract = buildViewBindingContract();
  assert.equal(contract.viewBindingId, "view_binding_contract_001");
  assert.equal(contract.bindings.length, 4);
});
