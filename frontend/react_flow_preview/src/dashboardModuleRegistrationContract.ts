import type { UnifiedVisualViewId } from "./unifiedVisualWorkspaceRegistry.js";

export type DashboardModuleKind =
  | "core_dashboard"
  | "client_dashboard"
  | "cube_dashboard"
  | "system_dashboard";

export type DashboardSurfaceTargetZone =
  | "left_navigation"
  | "center_viewport"
  | "right_context"
  | "top_communication"
  | "footer_status";

export type DashboardModuleSurfaceRegistration = {
  surfaceId: string;
  title: string;
  viewId: UnifiedVisualViewId;
  targetZone: DashboardSurfaceTargetZone;
  clientSelectable: boolean;
  enabledByDefault: boolean;
  requiresApproval: boolean;
};

export type DashboardModuleRegistrationContract = {
  moduleId: string;
  displayName: string;
  moduleKind: DashboardModuleKind;
  version: string;
  providedSurfaces: readonly DashboardModuleSurfaceRegistration[];
  registryDriven: true;
  appTsxHardcodingAllowed: false;
};

export type DashboardModuleRegistrationCandidate = Omit<
  DashboardModuleRegistrationContract,
  "registryDriven" | "appTsxHardcodingAllowed"
> & {
  registryDriven: boolean;
  appTsxHardcodingAllowed: boolean;
};

export type DashboardModuleRegistrationValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function validateDashboardModuleRegistration(
  registration: DashboardModuleRegistrationCandidate,
): DashboardModuleRegistrationValidation {
  const errors: string[] = [];

  if (!registration.moduleId.trim()) {
    errors.push("moduleId_required");
  }

  if (!registration.displayName.trim()) {
    errors.push("displayName_required");
  }

  if (!registration.version.trim()) {
    errors.push("version_required");
  }

  if (!registration.registryDriven) {
    errors.push("registry_driven_required");
  }

  if (registration.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (registration.providedSurfaces.length === 0) {
    errors.push("at_least_one_surface_required");
  }

  const seenSurfaceIds = new Set<string>();

  for (const surface of registration.providedSurfaces) {
    if (!surface.surfaceId.trim()) {
      errors.push("surfaceId_required");
    }

    if (seenSurfaceIds.has(surface.surfaceId)) {
      errors.push(`duplicate_surfaceId:${surface.surfaceId}`);
    }

    seenSurfaceIds.add(surface.surfaceId);

    if (!surface.title.trim()) {
      errors.push(`surface_title_required:${surface.surfaceId}`);
    }

    if (surface.targetZone === "center_viewport" && !surface.clientSelectable) {
      errors.push(`center_surface_must_be_client_selectable:${surface.surfaceId}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

export function buildDashboardModuleRegistrationContract(
  input: Omit<
    DashboardModuleRegistrationContract,
    "registryDriven" | "appTsxHardcodingAllowed"
  >,
): DashboardModuleRegistrationContract {
  return {
    ...input,
    registryDriven: true,
    appTsxHardcodingAllowed: false,
  };
}
