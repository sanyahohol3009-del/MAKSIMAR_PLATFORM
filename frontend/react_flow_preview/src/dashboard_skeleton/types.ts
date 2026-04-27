import type {
  DashboardModuleKind,
  DashboardSurfaceTargetZone,
} from "../dashboardModuleRegistrationContract.js";

export type DashboardSkeletonDomain =
  | "operator_core"
  | "foundation_truth"
  | "incident_diagnostics"
  | "visual_graphs"
  | "telemetry_charts"
  | "operator_interaction"
  | "memory_governance"
  | "project_context"
  | "server_runtime"
  | "network_security"
  | "family_presence"
  | "mobile_companion"
  | "smart_home"
  | "simulation_sandbox"
  | "physics_digital_twin"
  | "robotics_industrial"
  | "engineering_3d_cad_cam"
  | "content_growth_media"
  | "business_finance"
  | "system_settings";

export type DashboardSkeletonButtonGroup =
  | "home"
  | "foundation"
  | "incidents"
  | "graphs"
  | "telemetry"
  | "interaction"
  | "memory"
  | "project_context"
  | "server"
  | "security"
  | "family"
  | "mobile"
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
  | "memory_map_view"
  | "dependency_map_view"
  | "device_map_view"
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

export const DASHBOARD_SKELETON_BUTTON_GROUP_ORDER: readonly DashboardSkeletonButtonGroup[] = [
  "home",
  "foundation",
  "incidents",
  "graphs",
  "telemetry",
  "interaction",
  "memory",
  "project_context",
  "server",
  "security",
  "family",
  "mobile",
  "smart_home",
  "simulation",
  "robotics",
  "engineering",
  "media",
  "business",
  "settings",
];
