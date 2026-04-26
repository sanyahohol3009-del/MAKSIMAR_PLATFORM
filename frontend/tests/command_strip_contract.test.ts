import test from "node:test";
import assert from "node:assert/strict";

import { buildCommandStripContract } from "../contracts/command_strip_contract.js";

test("command strip contract builds", () => {
  const contract = buildCommandStripContract();
  assert.equal(contract.commandStripId, "command_strip_contract_001");
  assert.equal(contract.actions.length, 3);
  assert.equal(contract.directServerMutationAllowed, false);
});
