import assert from "node:assert/strict";
import test from "node:test";

import {
  buildDashboardModuleRegistrationContract,
  validateDashboardModuleRegistration,
} from "../react_flow_preview/src/dashboardModuleRegistrationContract.js";

test("dashboard module registration contract accepts registry-driven module", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "core_foundation_dashboard",
    displayName: "Core Foundation Dashboard",
    moduleKind: "core_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "foundation_topology",
        title: "Foundation Topology",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: true,
        requiresApproval: false,
      },
    ],
  });

  const validation = validateDashboardModuleRegistration(registration);

  assert.equal(registration.registryDriven, true);
  assert.equal(registration.appTsxHardcodingAllowed, false);
  assert.equal(validation.valid, true);
  assert.deepEqual(validation.errors, []);
});

test("dashboard module registration contract rejects app.tsx hardcoding", () => {
  const registration = {
    moduleId: "bad_dashboard",
    displayName: "Bad Dashboard",
    moduleKind: "client_dashboard" as const,
    version: "1.0.0",
    registryDriven: true as const,
    appTsxHardcodingAllowed: true as const,
    providedSurfaces: [
      {
        surfaceId: "bad_surface",
        title: "Bad Surface",
        viewId: "chart:node_resources" as const,
        targetZone: "center_viewport" as const,
        clientSelectable: true,
        enabledByDefault: true,
        requiresApproval: false,
      },
    ],
  };

  const validation = validateDashboardModuleRegistration(registration);

  assert.equal(validation.valid, false);
  assert.equal(validation.errors.includes("app_tsx_hardcoding_forbidden"), true);
});

test("dashboard module registration contract rejects duplicate surfaces", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "duplicate_dashboard",
    displayName: "Duplicate Dashboard",
    moduleKind: "cube_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "same_surface",
        title: "First Surface",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: true,
        requiresApproval: false,
      },
      {
        surfaceId: "same_surface",
        title: "Second Surface",
        viewId: "chart:node_resources",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: false,
        requiresApproval: false,
      },
    ],
  });

  const validation = validateDashboardModuleRegistration(registration);

  assert.equal(validation.valid, false);
  assert.equal(validation.errors.includes("duplicate_surfaceId:same_surface"), true);
});

test("dashboard module registration contract keeps center surface selectable", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "hidden_center_dashboard",
    displayName: "Hidden Center Dashboard",
    moduleKind: "client_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "hidden_center_surface",
        title: "Hidden Center Surface",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: false,
        enabledByDefault: true,
        requiresApproval: false,
      },
    ],
  });

  const validation = validateDashboardModuleRegistration(registration);

  assert.equal(validation.valid, false);
  assert.equal(
    validation.errors.includes(
      "center_surface_must_be_client_selectable:hidden_center_surface",
    ),
    true,
  );
});
