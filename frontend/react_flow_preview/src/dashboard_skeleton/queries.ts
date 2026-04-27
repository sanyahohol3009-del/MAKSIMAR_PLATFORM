import {
  DASHBOARD_SKELETON_BUTTON_GROUP_ORDER,
  type DashboardSkeletonButtonGroup,
  type DashboardSkeletonSurface,
  type DashboardSkeletonSurfaceGroup,
} from "./types.js";
import { DASHBOARD_SKELETON_SURFACE_TAXONOMY } from "./surfaces.js";

export function getDashboardSkeletonSurfaces(): readonly DashboardSkeletonSurface[] {
  return DASHBOARD_SKELETON_SURFACE_TAXONOMY;
}

export function getDashboardSkeletonSurfaceById(
  surfaceId: string,
): DashboardSkeletonSurface | null {
  return (
    DASHBOARD_SKELETON_SURFACE_TAXONOMY.find(
      (surface) => surface.surfaceId === surfaceId,
    ) ?? null
  );
}

export function getReservedAdapterSurfaces(): readonly DashboardSkeletonSurface[] {
  return DASHBOARD_SKELETON_SURFACE_TAXONOMY.filter(
    (surface) => surface.adapterBoundaryRequired,
  );
}

export function getMemoryControlSurfaces(): readonly DashboardSkeletonSurface[] {
  return DASHBOARD_SKELETON_SURFACE_TAXONOMY.filter(
    (surface) => surface.domain === "memory_governance",
  );
}

export function getMobileCompanionSurfaces(): readonly DashboardSkeletonSurface[] {
  return DASHBOARD_SKELETON_SURFACE_TAXONOMY.filter(
    (surface) => surface.domain === "mobile_companion",
  );
}

export function getButtonGroupTitle(
  buttonGroup: DashboardSkeletonButtonGroup,
): string {
  switch (buttonGroup) {
    case "home":
      return "Home";
    case "foundation":
      return "Foundation";
    case "incidents":
      return "Incidents / Diagnostics";
    case "graphs":
      return "Graphs";
    case "telemetry":
      return "Telemetry";
    case "interaction":
      return "Interaction";
    case "memory":
      return "Memory Control";
    case "project_context":
      return "Project Context";
    case "server":
      return "Server";
    case "security":
      return "Security";
    case "family":
      return "Family";
    case "mobile":
      return "Mobile Companion";
    case "smart_home":
      return "Smart Home";
    case "simulation":
      return "Simulation";
    case "robotics":
      return "Robotics";
    case "engineering":
      return "3D / Engineering";
    case "media":
      return "Media";
    case "business":
      return "Business";
    case "settings":
      return "Settings";
  }
}

export function groupDashboardSkeletonSurfacesByButtonGroup(): readonly DashboardSkeletonSurfaceGroup[] {
  return DASHBOARD_SKELETON_BUTTON_GROUP_ORDER.map((buttonGroup) => ({
    buttonGroup,
    title: getButtonGroupTitle(buttonGroup),
    surfaces: DASHBOARD_SKELETON_SURFACE_TAXONOMY.filter(
      (surface) => surface.buttonGroup === buttonGroup,
    ),
  })).filter((group) => group.surfaces.length > 0);
}
