import {
  buildDashboardSkeletonNavigationRendererRouteBindingReadModel,
  getDashboardSkeletonNavigationRendererRouteBySurfaceId,
} from "./dashboardSkeletonNavigationRendererRouteBinding.js";
import type {
  DashboardSkeletonNavigationRendererRoute,
} from "./dashboardSkeletonNavigationRendererRouteBinding.js";
import {
  getUnifiedVisualWorkspaceRegistryEntry,
  type UnifiedVisualViewId,
} from "./unifiedVisualWorkspaceRegistry.js";

export type PermanentRailActiveDashboardSelectionBindingTarget =
  "permanent_rail_active_dashboard_selection_binding";

export type PermanentRailActiveDashboardSelectionBindingSource =
  "dashboard_skeleton_navigation_renderer_route_binding";

export type PermanentRailActiveDashboardSelectionRouteStatus =
  | "center_viewport_ready"
  | "center_viewport_not_ready";

export type PermanentRailActiveDashboardSelectionRoute = {
  surfaceId: string;
  navigationId: string;
  title: string;
  viewId: string;
  activeView: UnifiedVisualViewId | null;
  routeStatus: PermanentRailActiveDashboardSelectionRouteStatus;
  rendererAdapterId: string;
  rendererAdapterKind: string;
  appTsxHardcodingAllowed: false;
};

export type PermanentRailActiveDashboardSelectionBindingReadModel = {
  target: PermanentRailActiveDashboardSelectionBindingTarget;
  source: PermanentRailActiveDashboardSelectionBindingSource;
  routes: readonly PermanentRailActiveDashboardSelectionRoute[];
  totalRoutes: number;
  centerViewportReadyRoutes: number;
  centerViewportNotReadyRoutes: number;
  defaultSurfaceId: "operator_home";
  appTsxHardcodingAllowed: false;
  manualDashboardButtonListAllowed: false;
  manualRendererRouteLogicAllowed: false;
};

export type PermanentRailActiveDashboardSelectionBindingValidation = {
  valid: boolean;
  errors: readonly string[];
};

const SURFACE_TO_VIEW_ID: Readonly<Record<string, UnifiedVisualViewId>> = {
  operator_home: "graph:topology",
  topology_graph: "graph:topology",
  dependency_graph: "graph:dependency",
  dataflow_graph: "graph:dataflow",
  module_graph: "graph:modules",
  truth_consistency_graph: "graph:truth_consistency",
  guard_chain_graph: "graph:guard_chain",
  workspace_graph: "graph:workspace",
  node_resources: "chart:node_resources",
  security_telemetry: "chart:security_telemetry",
  telemetry_summary: "chart:summary",
};

function readOptionalString(
  source: unknown,
  key: string,
): string | null {
  if (typeof source !== "object" || source === null) {
    return null;
  }

  const record = source as Readonly<Record<string, unknown>>;
  const value = record[key];

  return typeof value === "string" ? value : null;
}

function resolveUnifiedVisualViewId(viewId: string): UnifiedVisualViewId | null {
  try {
    getUnifiedVisualWorkspaceRegistryEntry(viewId as UnifiedVisualViewId);
    return viewId as UnifiedVisualViewId;
  } catch {
    return null;
  }
}

function resolveRouteViewId(
  route: DashboardSkeletonNavigationRendererRoute,
): string {
  return (
    readOptionalString(route.surface, "viewId") ??
    readOptionalString(route.surface, "activeView") ??
    readOptionalString(route.surface, "visualViewId") ??
    readOptionalString(route.navigationItem, "viewId") ??
    readOptionalString(route.navigationItem, "activeView") ??
    readOptionalString(route.navigationItem, "visualViewId") ??
    SURFACE_TO_VIEW_ID[route.surface.surfaceId] ??
    route.surface.surfaceId
  );
}

function buildSelectionRoute(
  route: DashboardSkeletonNavigationRendererRoute,
): PermanentRailActiveDashboardSelectionRoute {
  const viewId = resolveRouteViewId(route);
  const activeView = resolveUnifiedVisualViewId(viewId);

  return {
    surfaceId: route.surface.surfaceId,
    navigationId: route.navigationItem.navigationId,
    title: route.surface.title,
    viewId,
    activeView,
    routeStatus:
      activeView === null ? "center_viewport_not_ready" : "center_viewport_ready",
    rendererAdapterId: route.rendererAdapter.adapterId,
    rendererAdapterKind: route.rendererAdapter.adapterKind,
    appTsxHardcodingAllowed: false,
  };
}

export function buildPermanentRailActiveDashboardSelectionBindingReadModel(): PermanentRailActiveDashboardSelectionBindingReadModel {
  const routeBinding =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel();

  const routes = routeBinding.routes.map((route) => buildSelectionRoute(route));

  return {
    target: "permanent_rail_active_dashboard_selection_binding",
    source: "dashboard_skeleton_navigation_renderer_route_binding",
    routes,
    totalRoutes: routes.length,
    centerViewportReadyRoutes: routes.filter(
      (route) => route.routeStatus === "center_viewport_ready",
    ).length,
    centerViewportNotReadyRoutes: routes.filter(
      (route) => route.routeStatus === "center_viewport_not_ready",
    ).length,
    defaultSurfaceId: "operator_home",
    appTsxHardcodingAllowed: false,
    manualDashboardButtonListAllowed: false,
    manualRendererRouteLogicAllowed: false,
  };
}

export function getPermanentRailSelectionRouteBySurfaceId(
  surfaceId: string,
): PermanentRailActiveDashboardSelectionRoute | null {
  const route = getDashboardSkeletonNavigationRendererRouteBySurfaceId(surfaceId);

  if (!route) {
    return null;
  }

  return buildSelectionRoute(route);
}

export function getActiveViewForPermanentRailSurfaceId(
  surfaceId: string,
): UnifiedVisualViewId | null {
  const selectionRoute = getPermanentRailSelectionRouteBySurfaceId(surfaceId);

  if (!selectionRoute) {
    return null;
  }

  return selectionRoute.activeView;
}

export function validatePermanentRailActiveDashboardSelectionBindingReadModel(
  readModel: PermanentRailActiveDashboardSelectionBindingReadModel =
    buildPermanentRailActiveDashboardSelectionBindingReadModel(),
): PermanentRailActiveDashboardSelectionBindingValidation {
  const errors: string[] = [];
  const seenSurfaceIds = new Set<string>();

  if (readModel.target !== "permanent_rail_active_dashboard_selection_binding") {
    errors.push("target_must_be_permanent_rail_active_dashboard_selection_binding");
  }

  if (readModel.source !== "dashboard_skeleton_navigation_renderer_route_binding") {
    errors.push("source_must_be_dashboard_skeleton_navigation_renderer_route_binding");
  }

  if (readModel.totalRoutes !== 34) {
    errors.push("total_routes_must_be_34");
  }

  if (readModel.centerViewportReadyRoutes < 1) {
    errors.push("at_least_one_center_viewport_ready_route_required");
  }

  if (readModel.defaultSurfaceId !== "operator_home") {
    errors.push("default_surface_must_be_operator_home");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (readModel.manualDashboardButtonListAllowed) {
    errors.push("manual_dashboard_button_list_forbidden");
  }

  if (readModel.manualRendererRouteLogicAllowed) {
    errors.push("manual_renderer_route_logic_forbidden");
  }

  for (const route of readModel.routes) {
    if (seenSurfaceIds.has(route.surfaceId)) {
      errors.push(`duplicate_surface_route:${route.surfaceId}`);
    }

    seenSurfaceIds.add(route.surfaceId);

    if (route.appTsxHardcodingAllowed) {
      errors.push(`route_app_tsx_hardcoding_forbidden:${route.surfaceId}`);
    }

    if (route.routeStatus === "center_viewport_ready" && route.activeView === null) {
      errors.push(`ready_route_missing_active_view:${route.surfaceId}`);
    }

    if (route.activeView !== null) {
      try {
        getUnifiedVisualWorkspaceRegistryEntry(route.activeView);
      } catch {
        errors.push(`active_view_not_registered:${route.surfaceId}:${route.activeView}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
