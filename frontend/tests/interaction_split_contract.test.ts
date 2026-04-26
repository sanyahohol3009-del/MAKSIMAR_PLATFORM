import test from "node:test";
import assert from "node:assert/strict";

import { buildInteractionSplitContract } from "../contracts/interaction_split_contract.js";

test("interaction split contract builds", () => {
  const contract = buildInteractionSplitContract();
  assert.equal(contract.interactionSplitId, "interaction_split_contract_001");
  assert.equal(contract.splitMode, "chat_explain_command_ready");
  assert.equal(contract.guardedCommandPath, true);
});
