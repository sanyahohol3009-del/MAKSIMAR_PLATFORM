import type {
  DashboardSkeletonRenderMode,
  DashboardSkeletonSurface,
} from "../dashboard_skeleton/types.js";
import type {
  DashboardSurfaceTargetZone,
} from "../dashboardModuleRegistrationContract.js";

export type DashboardRendererAdapterKind =
  | "react_flow_graph_renderer"
  | "echarts_chart_renderer"
  | "panel_renderer"
  | "chat_surface_renderer"
  | "memory_map_renderer"
  | "three_d_scene_renderer"
  | "simulation_scene_renderer"
  | "external_placeholder_renderer";

export type DashboardRendererBindingPolicy = "adapter_boundary_only";

export type DashboardRendererSafetyMode =
  | "read_only_visualization"
  | "guarded_interactive_preview";

export type DashboardRendererAdapterContract = {
  adapterId: string;
  title: string;
  adapterKind: DashboardRendererAdapterKind;
  supportedRenderModes: readonly DashboardSkeletonRenderMode[];
  supportedTargetZones: readonly DashboardSurfaceTargetZone[];
  centerViewportCompatible: boolean;
  appTsxHardcodingAllowed: false;
  directEngineBindingAllowed: false;
  bindingPolicy: DashboardRendererBindingPolicy;
  safetyMode: DashboardRendererSafetyMode;
  description: string;
};

export type DashboardRendererResolution = {
  surface: DashboardSkeletonSurface;
  adapter: DashboardRendererAdapterContract;
  resolved: true;
};

export type DashboardRendererValidation = {
  valid: boolean;
  errors: readonly string[];
};
