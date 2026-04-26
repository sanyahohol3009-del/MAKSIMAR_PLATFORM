import test from "node:test";
import assert from "node:assert/strict";
import { buildPanelNavigationInspectPresentation } from "../react_flow_preview/src/panelNavigationShellInspect.js";

test("panel navigation inspect builds foundation panel binding", () => {
  const inspect = buildPanelNavigationInspectPresentation("system_status");

  assert.equal(inspect.title, "System Status");
  assert.equal(inspect.semanticKind, "panel_navigation_binding");
  assert.equal(inspect.sections.length, 2);
  assert.equal(inspect.sections[0]?.items.length, 3);
});

test("panel navigation inspect builds operator panel binding", () => {
  const inspect = buildPanelNavigationInspectPresentation("approval_queue");

  assert.equal(inspect.title, "Approval Queue");
  assert.equal(inspect.sections[1]?.items[0]?.value, "workspace_operator_interaction");
});
