import test from "node:test";
import assert from "node:assert/strict";

import { buildDashboardShellContract } from "../contracts/dashboard_shell_contract.js";

test("dashboard shell contract builds", () => {
  const contract = buildDashboardShellContract();
  assert.equal(contract.shellId, "dashboard_shell_contract_001");
  assert.equal(contract.operatorVisible, true);
  assert.equal(contract.truthBound, true);
});
