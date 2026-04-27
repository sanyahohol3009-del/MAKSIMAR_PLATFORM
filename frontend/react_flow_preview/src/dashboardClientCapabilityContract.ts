import type {
  DashboardModuleKind,
  DashboardModuleRegistrationContract,
  DashboardModuleSurfaceRegistration,
  DashboardSurfaceTargetZone,
} from "./dashboardModuleRegistrationContract.js";
import type { UnifiedVisualViewId } from "./unifiedVisualWorkspaceRegistry.js";

export type DashboardClientCapabilityMode = "strict";

export type DashboardFeatureGateRejectReason =
  | "module_kind_not_allowed"
  | "module_disabled"
  | "module_not_approved"
  | "target_zone_not_allowed"
  | "view_not_allowed"
  | "surface_requires_approval"
  | "center_surface_not_client_selectable";

export type DashboardClientCapabilityProfile = {
  clientId: string;
  capabilityMode: DashboardClientCapabilityMode;
  allowedModuleKinds: readonly DashboardModuleKind[];
  allowedTargetZones: readonly DashboardSurfaceTargetZone[];
  allowedViewIds: readonly UnifiedVisualViewId[] | "all";
  approvedModuleIds: readonly string[] | "all";
  disabledModuleIds: readonly string[];
  approvedSurfaceIds: readonly string[];
};

export type DashboardFeatureGateSurfaceDecision = {
  surface: DashboardModuleSurfaceRegistration;
  allowed: boolean;
  reason: DashboardFeatureGateRejectReason | null;
};

export type DashboardFeatureGateResult = {
  clientId: string;
  moduleId: string;
  moduleAllowed: boolean;
  rejectedModuleReason: DashboardFeatureGateRejectReason | null;
  allowedSurfaces: readonly DashboardModuleSurfaceRegistration[];
  rejectedSurfaces: readonly DashboardFeatureGateSurfaceDecision[];
};

function isModuleApproved(
  approvedModuleIds: readonly string[] | "all",
  moduleId: string,
): boolean {
  return approvedModuleIds === "all" || approvedModuleIds.includes(moduleId);
}

function isViewAllowed(
  allowedViewIds: readonly UnifiedVisualViewId[] | "all",
  viewId: UnifiedVisualViewId,
): boolean {
  return allowedViewIds === "all" || allowedViewIds.includes(viewId);
}

function resolveModuleRejectReason(
  registration: DashboardModuleRegistrationContract,
  profile: DashboardClientCapabilityProfile,
): DashboardFeatureGateRejectReason | null {
  if (!profile.allowedModuleKinds.includes(registration.moduleKind)) {
    return "module_kind_not_allowed";
  }

  if (profile.disabledModuleIds.includes(registration.moduleId)) {
    return "module_disabled";
  }

  if (!isModuleApproved(profile.approvedModuleIds, registration.moduleId)) {
    return "module_not_approved";
  }

  return null;
}

function resolveSurfaceRejectReason(
  surface: DashboardModuleSurfaceRegistration,
  profile: DashboardClientCapabilityProfile,
): DashboardFeatureGateRejectReason | null {
  if (!profile.allowedTargetZones.includes(surface.targetZone)) {
    return "target_zone_not_allowed";
  }

  if (!isViewAllowed(profile.allowedViewIds, surface.viewId)) {
    return "view_not_allowed";
  }

  if (surface.targetZone === "center_viewport" && !surface.clientSelectable) {
    return "center_surface_not_client_selectable";
  }

  if (
    surface.requiresApproval &&
    !profile.approvedSurfaceIds.includes(surface.surfaceId)
  ) {
    return "surface_requires_approval";
  }

  return null;
}

export function evaluateDashboardModuleForClient(
  registration: DashboardModuleRegistrationContract,
  profile: DashboardClientCapabilityProfile,
): DashboardFeatureGateResult {
  const rejectedModuleReason = resolveModuleRejectReason(registration, profile);

  if (rejectedModuleReason) {
    return {
      clientId: profile.clientId,
      moduleId: registration.moduleId,
      moduleAllowed: false,
      rejectedModuleReason,
      allowedSurfaces: [],
      rejectedSurfaces: registration.providedSurfaces.map((surface) => ({
        surface,
        allowed: false,
        reason: rejectedModuleReason,
      })),
    };
  }

  const allowedSurfaces: DashboardModuleSurfaceRegistration[] = [];
  const rejectedSurfaces: DashboardFeatureGateSurfaceDecision[] = [];

  for (const surface of registration.providedSurfaces) {
    const reason = resolveSurfaceRejectReason(surface, profile);

    if (reason) {
      rejectedSurfaces.push({
        surface,
        allowed: false,
        reason,
      });
      continue;
    }

    allowedSurfaces.push(surface);
  }

  return {
    clientId: profile.clientId,
    moduleId: registration.moduleId,
    moduleAllowed: allowedSurfaces.length > 0,
    rejectedModuleReason: null,
    allowedSurfaces,
    rejectedSurfaces,
  };
}
