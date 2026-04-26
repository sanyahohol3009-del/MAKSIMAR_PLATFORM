import test from "node:test";
import assert from "node:assert/strict";

import { buildTopStatusBarContract } from "../contracts/top_status_bar_contract.js";

test("top status bar contract builds", () => {
  const contract = buildTopStatusBarContract();
  assert.equal(contract.topStatusBarId, "top_status_bar_contract_001");
  assert.equal(contract.signals.length, 3);
});
