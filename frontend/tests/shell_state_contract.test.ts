import test from "node:test";
import assert from "node:assert/strict";

import { buildShellStateContract } from "../contracts/shell_state_contract.js";

test("shell state contract builds", () => {
  const contract = buildShellStateContract();
  assert.equal(contract.shellStateId, "shell_state_contract_001");
  assert.equal(contract.stateMode, "registry_state_ready");
});
