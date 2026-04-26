import test from "node:test";
import assert from "node:assert/strict";
import {
  getPanelNavigationGroups,
  getPanelNavigationOrder,
  getPanelNavigationRegistryEntry,
  panelNavigationRegistry,
} from "../react_flow_preview/src/panelNavigationRegistry.js";

test("panel navigation registry exposes stable canonical order", () => {
  assert.deepEqual(getPanelNavigationOrder(), [
    "system_status",
    "guard_chain",
    "incidents",
    "logs",
    "topology",
    "action_queue",
    "approval_queue",
    "audit_timeline",
  ]);
});

test("panel navigation registry contains eight confirmed panels", () => {
  assert.equal(panelNavigationRegistry.length, 8);
});

test("panel navigation groups preserve audited view grouping", () => {
  const groups = getPanelNavigationGroups();

  assert.deepEqual(
    groups.map((group) => group.navigationViewId),
    [
      "view_foundation_status",
      "view_foundation_observability",
      "view_operator_interaction",
    ],
  );

  assert.deepEqual(groups[0]?.panelIds, [
    "system_status",
    "guard_chain",
    "incidents",
  ]);

  assert.deepEqual(groups[1]?.panelIds, [
    "logs",
    "topology",
  ]);

  assert.deepEqual(groups[2]?.panelIds, [
    "action_queue",
    "approval_queue",
    "audit_timeline",
  ]);
});

test("panel navigation registry resolves operator interaction panel", () => {
  const entry = getPanelNavigationRegistryEntry("approval_queue");
  assert.equal(entry.workspaceId, "workspace_operator_interaction");
  assert.equal(
    entry.bindingReason,
    "operator_interaction_visibility",
  );
  assert.equal(
    entry.shellLanding,
    "main_operator_primary_operator_interaction",
  );
});
