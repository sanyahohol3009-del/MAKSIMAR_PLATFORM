import assert from "node:assert/strict";
import test from "node:test";

import {
  buildDashboardModuleRegistrationContract,
} from "../react_flow_preview/src/dashboardModuleRegistrationContract.js";
import {
  evaluateDashboardModuleForClient,
  type DashboardClientCapabilityProfile,
} from "../react_flow_preview/src/dashboardClientCapabilityContract.js";

const baseProfile: DashboardClientCapabilityProfile = {
  clientId: "client_family_base",
  capabilityMode: "strict",
  allowedModuleKinds: ["core_dashboard", "client_dashboard", "cube_dashboard"],
  allowedTargetZones: ["left_navigation", "center_viewport", "right_context"],
  allowedViewIds: "all",
  approvedModuleIds: "all",
  disabledModuleIds: [],
  approvedSurfaceIds: [],
};

test("dashboard client capability allows approved registry-driven module", () => {
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

  const result = evaluateDashboardModuleForClient(registration, baseProfile);

  assert.equal(result.moduleAllowed, true);
  assert.equal(result.rejectedModuleReason, null);
  assert.equal(result.allowedSurfaces.length, 1);
  assert.equal(result.rejectedSurfaces.length, 0);
});

test("dashboard client capability rejects disallowed module kind", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "system_only_dashboard",
    displayName: "System Only Dashboard",
    moduleKind: "system_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "system_surface",
        title: "System Surface",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: true,
        requiresApproval: false,
      },
    ],
  });

  const result = evaluateDashboardModuleForClient(registration, baseProfile);

  assert.equal(result.moduleAllowed, false);
  assert.equal(result.rejectedModuleReason, "module_kind_not_allowed");
  assert.equal(result.allowedSurfaces.length, 0);
  assert.equal(result.rejectedSurfaces.length, 1);

  const rejectedSurface = result.rejectedSurfaces[0];
  if (!rejectedSurface) {
    throw new Error("expected rejected surface");
  }

  assert.equal(rejectedSurface.reason, "module_kind_not_allowed");
});

test("dashboard client capability requires approval for protected surfaces", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "robotics_cube_dashboard",
    displayName: "Robotics Cube Dashboard",
    moduleKind: "cube_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "robotics_simulation_surface",
        title: "Robotics Simulation Surface",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: false,
        requiresApproval: true,
      },
    ],
  });

  const blockedResult = evaluateDashboardModuleForClient(
    registration,
    baseProfile,
  );

  assert.equal(blockedResult.moduleAllowed, false);
  assert.equal(blockedResult.allowedSurfaces.length, 0);
  assert.equal(blockedResult.rejectedSurfaces.length, 1);

  const blockedSurface = blockedResult.rejectedSurfaces[0];
  if (!blockedSurface) {
    throw new Error("expected blocked surface");
  }

  assert.equal(blockedSurface.reason, "surface_requires_approval");

  const approvedResult = evaluateDashboardModuleForClient(registration, {
    ...baseProfile,
    approvedSurfaceIds: ["robotics_simulation_surface"],
  });

  assert.equal(approvedResult.moduleAllowed, true);
  assert.equal(approvedResult.allowedSurfaces.length, 1);
});

test("dashboard client capability filters disallowed target zones and views", () => {
  const registration = buildDashboardModuleRegistrationContract({
    moduleId: "mixed_dashboard",
    displayName: "Mixed Dashboard",
    moduleKind: "client_dashboard",
    version: "1.0.0",
    providedSurfaces: [
      {
        surfaceId: "allowed_surface",
        title: "Allowed Surface",
        viewId: "graph:topology",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: true,
        requiresApproval: false,
      },
      {
        surfaceId: "footer_surface",
        title: "Footer Surface",
        viewId: "graph:topology",
        targetZone: "footer_status",
        clientSelectable: false,
        enabledByDefault: false,
        requiresApproval: false,
      },
      {
        surfaceId: "blocked_chart_surface",
        title: "Blocked Chart Surface",
        viewId: "chart:node_resources",
        targetZone: "center_viewport",
        clientSelectable: true,
        enabledByDefault: false,
        requiresApproval: false,
      },
    ],
  });

  const result = evaluateDashboardModuleForClient(registration, {
    ...baseProfile,
    allowedViewIds: ["graph:topology"],
  });

  assert.equal(result.moduleAllowed, true);
  assert.equal(result.allowedSurfaces.length, 1);
  assert.equal(result.rejectedSurfaces.length, 2);

  const allowedSurface = result.allowedSurfaces[0];
  const firstRejectedSurface = result.rejectedSurfaces[0];
  const secondRejectedSurface = result.rejectedSurfaces[1];

  if (!allowedSurface) {
    throw new Error("expected allowed surface");
  }

  if (!firstRejectedSurface) {
    throw new Error("expected first rejected surface");
  }

  if (!secondRejectedSurface) {
    throw new Error("expected second rejected surface");
  }

  assert.equal(allowedSurface.surfaceId, "allowed_surface");
  assert.equal(firstRejectedSurface.reason, "target_zone_not_allowed");
  assert.equal(secondRejectedSurface.reason, "view_not_allowed");
});
