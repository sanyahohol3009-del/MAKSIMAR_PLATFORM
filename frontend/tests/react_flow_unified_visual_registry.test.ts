import test from "node:test";
import assert from "node:assert/strict";
import {
  getUnifiedVisualRegistryGroups,
  getUnifiedVisualViewOrder,
  getUnifiedVisualWorkspaceRegistryEntry,
  unifiedVisualWorkspaceRegistry,
} from "../react_flow_preview/src/unifiedVisualWorkspaceRegistry.js";

test("unified visual registry exposes stable graph-plus-chart order", () => {
  assert.deepEqual(getUnifiedVisualViewOrder(), [
    "graph:topology",
    "graph:dependency",
    "graph:dataflow",
    "graph:modules",
    "graph:guard_chain",
    "graph:truth_consistency",
    "graph:workspace",
    "graph:displays",
    "chart:node_resources",
    "chart:export_validation_assets",
    "chart:security_telemetry",
    "chart:summary",
  ]);
});

test("unified visual registry contains twelve entries", () => {
  assert.equal(unifiedVisualWorkspaceRegistry.length, 12);
});

test("unified visual registry exposes telemetry chart group", () => {
  const groups = getUnifiedVisualRegistryGroups();
  assert.deepEqual(
    groups.map((group) => group.group),
    [
      "execution_graphs",
      "operator_graphs",
      "foundation_graphs",
      "display_graphs",
      "telemetry_charts",
    ],
  );
  assert.equal(groups.at(-1)?.viewIds.length, 4);
});

test("unified visual registry resolves chart entry metadata", () => {
  const entry = getUnifiedVisualWorkspaceRegistryEntry("chart:node_resources");
  assert.equal(entry.viewKind, "chart");
  assert.equal(entry.group, "telemetry_charts");
  assert.equal(entry.summaryLabel, "Series Points");
  assert.equal(entry.summaryValue, 4);
});
