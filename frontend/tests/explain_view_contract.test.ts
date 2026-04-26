import test from "node:test";
import assert from "node:assert/strict";

import { buildExplainViewContract } from "../contracts/explain_view_contract.js";

test("explain view contract builds", () => {
  const contract = buildExplainViewContract();
  assert.equal(contract.explainViewId, "explain_view_contract_001");
  assert.equal(contract.blocks.length, 3);
});
