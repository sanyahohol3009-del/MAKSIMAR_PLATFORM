import test from "node:test";
import assert from "node:assert/strict";

import { graphProjectionRegistry } from "../react_flow_preview/src/graphProjectionData.js";

test("guard chain graph keeps canonical scope order", () => {
  const titles = graphProjectionRegistry.guard_chain.nodes.map((node) => node.title);

  assert.deepEqual(titles, [
    "Runtime Core",
    "Stop-Gate Watcher",
    "Core Guard",
    "Kernel Watchdog",
  ]);
});

test("truth consistency graph exposes canonical panel ids", () => {
  const panelIds = graphProjectionRegistry.truth_consistency.nodes.map(
    (node) => node.fields.find((field) => field.key === "panel_id")?.value,
  );

  assert.deepEqual(panelIds, [
    "panel_foundation_runtime_status_001",
    "panel_foundation_guard_status_001",
    "panel_foundation_core_guard_status_001",
    "panel_foundation_kernel_guard_status_001",
  ]);
});

test("workspace graph exposes three display nodes", () => {
  const displayNodes = graphProjectionRegistry.workspace.nodes.filter(
    (node) => node.semanticKind === "workspace_display_node",
  );

  assert.equal(displayNodes.length, 3);
});

test("display assignment graph exposes four assignment edges", () => {
  assert.equal(graphProjectionRegistry.displays.edges.length, 4);
});
