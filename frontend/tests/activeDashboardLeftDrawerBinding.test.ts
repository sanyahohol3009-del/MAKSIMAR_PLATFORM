import assert from "node:assert/strict";
import test from "node:test";

import {
  buildActiveDashboardLeftDrawerReadModel,
  getActiveDashboardLeftDrawerSectionByAlias,
  validateActiveDashboardLeftDrawerReadModel,
} from "../react_flow_preview/src/activeDashboardLeftDrawerBinding.js";

test("active dashboard left drawer binding validates operator home", () => {
  const readModel = buildActiveDashboardLeftDrawerReadModel({
    activeSurfaceId: "operator_home",
    activeView: "graph:topology",
  });

  const validation = validateActiveDashboardLeftDrawerReadModel(readModel);

  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
  assert.equal(readModel.totalSections, 3);
  assert.equal(readModel.permanentRailIsDashboardSelector, true);
  assert.equal(readModel.leftDrawerIsActiveDashboardContext, true);
});

test("active dashboard left drawer binding exposes functions settings and tools", () => {
  const readModel = buildActiveDashboardLeftDrawerReadModel({
    activeSurfaceId: "operator_home",
    activeView: "graph:topology",
  });

  assert.deepEqual(
    readModel.sections.map((section) => section.sectionId),
    ["functions", "settings", "tools"],
  );
});

test("active dashboard left drawer binding maps compatibility aliases", () => {
  const readModel = buildActiveDashboardLeftDrawerReadModel({
    activeSurfaceId: "operator_home",
    activeView: "graph:topology",
  });

  assert.equal(
    getActiveDashboardLeftDrawerSectionByAlias(
      readModel,
      "visual_registry_navigation",
    ).sectionId,
    "functions",
  );
  assert.equal(
    getActiveDashboardLeftDrawerSectionByAlias(readModel, "panel_navigation")
      .sectionId,
    "settings",
  );
  assert.equal(
    getActiveDashboardLeftDrawerSectionByAlias(
      readModel,
      "embedded_chat_context",
    ).sectionId,
    "tools",
  );
});

test("active dashboard left drawer binding remains non-executing", () => {
  const readModel = buildActiveDashboardLeftDrawerReadModel({
    activeSurfaceId: "operator_home",
    activeView: "graph:topology",
  });

  assert.equal(readModel.executableActionsAllowed, false);

  for (const section of readModel.sections) {
    for (const item of section.items) {
      assert.equal(item.executable, false);
    }
  }
});

test("active dashboard left drawer binding supports not-ready surfaces", () => {
  const readModel = buildActiveDashboardLeftDrawerReadModel({
    activeSurfaceId: "displays_graph",
    activeView: "graph:topology",
  });

  const validation = validateActiveDashboardLeftDrawerReadModel(readModel);

  assert.equal(validation.valid, true);
  assert.equal(readModel.leftDrawerIsActiveDashboardContext, true);
});
