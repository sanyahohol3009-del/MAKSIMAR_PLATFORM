import type {
  DashboardModuleKind,
  DashboardSurfaceTargetZone,
} from "./dashboardModuleRegistrationContract.js";

export type DashboardSkeletonDomain =
  | "operator_core"
  | "server_runtime"
  | "network_security"
  | "memory_knowledge"
  | "automation_commands"
  | "family_presence"
  | "smart_home"
  | "physics_simulation"
  | "robotics"
  | "engineering_3d_cad_cam"
  | "content_growth_media"
  | "business_finance"
  | "system_settings";

export type DashboardSkeletonButtonGroup =
  | "home"
  | "server"
  | "security"
  | "memory"
  | "commands"
  | "family"
  | "smart_home"
  | "simulation"
  | "robotics"
  | "engineering"
  | "media"
  | "business"
  | "settings";

export type DashboardSkeletonRenderMode =
  | "graph_view"
  | "chart_view"
  | "status_panel"
  | "table_panel"
  | "timeline_panel"
  | "chat_surface"
  | "three_d_scene_adapter"
  | "simulation_scene_adapter"
  | "external_adapter_placeholder";

export type DashboardSkeletonSurfaceStatus =
  | "implemented"
  | "reserved";

export type DashboardSkeletonSurface = {
  surfaceId: string;
  title: string;
  domain: DashboardSkeletonDomain;
  moduleKind: DashboardModuleKind;
  targetZone: DashboardSurfaceTargetZone;
  buttonGroup: DashboardSkeletonButtonGroup;
  renderMode: DashboardSkeletonRenderMode;
  status: DashboardSkeletonSurfaceStatus;
  clientSelectable: boolean;
  requiresApproval: boolean;
  adapterBoundaryRequired: boolean;
  description: string;
};

export type DashboardSkeletonSurfaceGroup = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  surfaces: readonly DashboardSkeletonSurface[];
};

export type DashboardSkeletonTaxonomyValidation = {
  valid: boolean;
  errors: readonly string[];
};

export const DASHBOARD_SKELETON_SURFACE_TAXONOMY: readonly DashboardSkeletonSurface[] = [
  {
    surfaceId: "operator_home",
    title: "Operator Home",
    domain: "operator_core",
    moduleKind: "core_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "home",
    renderMode: "graph_view",
    status: "implemented",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Main operator landing surface for the current dashboard shell.",
  },
  {
    surfaceId: "server_runtime",
    title: "Server Runtime",
    domain: "server_runtime",
    moduleKind: "core_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "server",
    renderMode: "chart_view",
    status: "implemented",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Server/runtime resource and health surface.",
  },
  {
    surfaceId: "network_security",
    title: "Network / Security",
    domain: "network_security",
    moduleKind: "system_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "security",
    renderMode: "graph_view",
    status: "implemented",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: false,
    description: "Security, topology, guard chain, network and trust-boundary surface.",
  },
  {
    surfaceId: "memory_knowledge",
    title: "Memory / Knowledge",
    domain: "memory_knowledge",
    moduleKind: "core_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "memory",
    renderMode: "table_panel",
    status: "implemented",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Memory, knowledge exposure, project context and provenance surface.",
  },
  {
    surfaceId: "command_control",
    title: "Commands / Approval",
    domain: "automation_commands",
    moduleKind: "core_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "commands",
    renderMode: "timeline_panel",
    status: "implemented",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Command queue, approval, handoff and operator action surface.",
  },
  {
    surfaceId: "family_presence",
    title: "Family / Presence",
    domain: "family_presence",
    moduleKind: "client_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "family",
    renderMode: "status_panel",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Family presence, household status and safe family dashboard surface.",
  },
  {
    surfaceId: "smart_home",
    title: "Smart Home",
    domain: "smart_home",
    moduleKind: "client_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "smart_home",
    renderMode: "status_panel",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: false,
    description: "Smart home dashboard surface for future device/state integration.",
  },
  {
    surfaceId: "physics_simulation",
    title: "Physics / Simulation",
    domain: "physics_simulation",
    moduleKind: "cube_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "simulation",
    renderMode: "simulation_scene_adapter",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: true,
    description: "Reserved simulation scene surface for future physics/digital twin viewport.",
  },
  {
    surfaceId: "robotics_control",
    title: "Robotics",
    domain: "robotics",
    moduleKind: "cube_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "robotics",
    renderMode: "simulation_scene_adapter",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: true,
    description: "Reserved robotics dashboard surface for future robot/telemetry visualization.",
  },
  {
    surfaceId: "engineering_3d_cad_cam",
    title: "3D / CAD / CAM",
    domain: "engineering_3d_cad_cam",
    moduleKind: "cube_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "engineering",
    renderMode: "three_d_scene_adapter",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: true,
    description: "Reserved 3D renderer surface for CAD/CAM/model/scene visualization.",
  },
  {
    surfaceId: "content_growth_media",
    title: "Content / Media",
    domain: "content_growth_media",
    moduleKind: "cube_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "media",
    renderMode: "timeline_panel",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: false,
    adapterBoundaryRequired: false,
    description: "Reserved content engine, media, growth and publishing dashboard surface.",
  },
  {
    surfaceId: "business_finance",
    title: "Business / Finance",
    domain: "business_finance",
    moduleKind: "client_dashboard",
    targetZone: "center_viewport",
    buttonGroup: "business",
    renderMode: "chart_view",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: false,
    description: "Reserved business, finance, billing, package and client delivery surface.",
  },
  {
    surfaceId: "system_settings",
    title: "System Settings",
    domain: "system_settings",
    moduleKind: "system_dashboard",
    targetZone: "right_context",
    buttonGroup: "settings",
    renderMode: "table_panel",
    status: "reserved",
    clientSelectable: true,
    requiresApproval: true,
    adapterBoundaryRequired: false,
    description: "Reserved settings/configuration dashboard surface.",
  },
];

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

export function getButtonGroupTitle(
  buttonGroup: DashboardSkeletonButtonGroup,
): string {
  switch (buttonGroup) {
    case "home":
      return "Home";
    case "server":
      return "Server";
    case "security":
      return "Security";
    case "memory":
      return "Memory";
    case "commands":
      return "Commands";
    case "family":
      return "Family";
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
  const groups: DashboardSkeletonSurfaceGroup[] = [];

  for (const surface of DASHBOARD_SKELETON_SURFACE_TAXONOMY) {
    let group = groups.find((item) => item.buttonGroup === surface.buttonGroup);

    if (!group) {
      group = {
        buttonGroup: surface.buttonGroup,
        title: getButtonGroupTitle(surface.buttonGroup),
        surfaces: [],
      };

      groups.push(group);
    }

    (group.surfaces as DashboardSkeletonSurface[]).push(surface);
  }

  return groups;
}

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
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
