import test from "node:test";
import assert from "node:assert/strict";

import { buildWorkspaceSwitchContract } from "../contracts/workspace_switch_contract.js";

test("workspace switch contract builds", () => {
  const contract = buildWorkspaceSwitchContract();
  assert.equal(contract.workspaceSwitchId, "workspace_switch_contract_001");
  assert.equal(contract.targets.length, 2);
  assert.equal(contract.guardedSwitching, true);
});
