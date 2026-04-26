import test from "node:test";
import assert from "node:assert/strict";

import { buildWorkspaceFrameContract } from "../contracts/workspace_frame_contract.js";

test("workspace frame contract builds", () => {
  const contract = buildWorkspaceFrameContract();
  assert.equal(contract.workspaceFrameId, "workspace_frame_contract_001");
  assert.equal(contract.zones.length, 4);
});
