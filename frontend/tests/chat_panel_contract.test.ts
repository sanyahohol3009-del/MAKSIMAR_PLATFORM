import test from "node:test";
import assert from "node:assert/strict";

import { buildChatPanelContract } from "../contracts/chat_panel_contract.js";

test("chat panel contract builds", () => {
  const contract = buildChatPanelContract();
  assert.equal(contract.chatPanelId, "chat_panel_contract_001");
  assert.equal(contract.visibleMessages.length, 2);
});
