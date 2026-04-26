import test from "node:test";
import assert from "node:assert/strict";

import { buildCommandQueueViewContract } from "../contracts/command_queue_view_contract.js";

test("command queue view contract builds", () => {
  const contract = buildCommandQueueViewContract();
  assert.equal(contract.commandQueueViewId, "command_queue_view_contract_001");
  assert.equal(contract.queueEntries.length, 3);
});
