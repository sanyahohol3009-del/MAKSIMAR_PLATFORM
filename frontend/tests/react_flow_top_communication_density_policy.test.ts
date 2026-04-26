import test from "node:test";
import assert from "node:assert/strict";
import { buildTopCommunicationDensityPolicy } from "../react_flow_preview/src/operator_shell/topCommunicationDensityPolicy.js";

test("top communication density policy makes content dominant in normalized mode", () => {
  const policy = buildTopCommunicationDensityPolicy("normalized_density");

  const content = policy.find((row) => row.blockId === "content_stream");
  const supportMeta = policy.find((row) => row.blockId === "support_meta");

  assert.equal(content?.state, "dominant");
  assert.equal(supportMeta?.state, "hidden");
});

test("top communication density policy keeps summary chips visible in baseline mode", () => {
  const policy = buildTopCommunicationDensityPolicy("baseline_density");

  const summary = policy.find((row) => row.blockId === "summary_chip_lane");
  assert.equal(summary?.state, "visible");
});
