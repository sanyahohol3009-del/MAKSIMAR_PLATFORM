import type { DashboardSkeletonTaxonomyValidation } from "./types.js";
import { DASHBOARD_SKELETON_SURFACE_TAXONOMY } from "./surfaces.js";

export function validateDashboardSkeletonSurfaceTaxonomy(): DashboardSkeletonTaxonomyValidation {
  const errors: string[] = [];
  const seenSurfaceIds = new Set<string>();

  for (const surface of DASHBOARD_SKELETON_SURFACE_TAXONOMY) {
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

    if (
      (surface.renderMode === "three_d_scene_adapter" ||
        surface.renderMode === "simulation_scene_adapter") &&
      !surface.adapterBoundaryRequired
    ) {
      errors.push(`adapter_boundary_required:${surface.surfaceId}`);
    }

    if (
      surface.domain === "mobile_companion" &&
      surface.buttonGroup === "family"
    ) {
      errors.push(`mobile_companion_must_not_live_in_family:${surface.surfaceId}`);
    }

    if (
      surface.domain === "memory_governance" &&
      surface.buttonGroup !== "memory"
    ) {
      errors.push(`memory_surface_must_live_in_memory_group:${surface.surfaceId}`);
    }
  }

  if (
    !DASHBOARD_SKELETON_SURFACE_TAXONOMY.some(
      (surface) => surface.surfaceId === "memory_control_dashboard",
    )
  ) {
    errors.push("memory_control_dashboard_required");
  }

  if (
    !DASHBOARD_SKELETON_SURFACE_TAXONOMY.some(
      (surface) => surface.surfaceId === "mobile_companion_android",
    )
  ) {
    errors.push("mobile_companion_android_required");
  }

  if (
    !DASHBOARD_SKELETON_SURFACE_TAXONOMY.some(
      (surface) => surface.surfaceId === "mobile_companion_ios",
    )
  ) {
    errors.push("mobile_companion_ios_required");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
