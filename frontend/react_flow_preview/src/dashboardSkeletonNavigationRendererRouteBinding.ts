import type {
  DashboardSkeletonNavigationBindingReadModel,
  DashboardSkeletonNavigationItem,
} from "./dashboardSkeletonNavigationBinding.js";
import {
  buildDashboardSkeletonNavigationBindingReadModel,
  getDashboardSkeletonNavigationItemBySurfaceId,
} from "./dashboardSkeletonNavigationBinding.js";
import type {
  DashboardSkeletonSurface,
} from "./dashboardSkeletonSurfaceTaxonomy.js";
import {
  getDashboardSkeletonSurfaceById,
} from "./dashboardSkeletonSurfaceTaxonomy.js";
import type {
  DashboardRendererAdapterContract,
} from "./dashboardRendererAdapterBoundary.js";
import {
  resolveDashboardRendererAdapterForSurface,
} from "./dashboardRendererAdapterBoundary.js";

export type DashboardSkeletonNavigationRendererRouteSource =
  "dashboard_skeleton_navigation_binding";

export type DashboardSkeletonNavigationRendererRouteBindingReadModel = {
  source: DashboardSkeletonNavigationRendererRouteSource;
  navigationReadModel: DashboardSkeletonNavigationBindingReadModel;
  routes: readonly DashboardSkeletonNavigationRendererRoute[];
  totalRoutes: number;
  adapterBoundaryRoutes: number;
  threeDRendererRoutes: number;
  simulationRendererRoutes: number;
  memoryRendererRoutes: number;
  appTsxHardcodingAllowed: false;
  directEngineBindingAllowed: false;
};

export type DashboardSkeletonNavigationRendererRoute = {
  routeId: string;
  navigationItem: DashboardSkeletonNavigationItem;
  surface: DashboardSkeletonSurface;
  rendererAdapter: DashboardRendererAdapterContract;
  source: DashboardSkeletonNavigationRendererRouteSource;
  appTsxHardcodingAllowed: false;
  directEngineBindingAllowed: false;
};

export type DashboardSkeletonNavigationRendererRouteValidation = {
  valid: boolean;
  errors: readonly string[];
};

function buildNavigationRendererRoute(
  navigationItem: DashboardSkeletonNavigationItem,
): DashboardSkeletonNavigationRendererRoute {
  const surface = getDashboardSkeletonSurfaceById(navigationItem.surfaceId);

  if (!surface) {
    throw new Error(`dashboard_surface_not_found:${navigationItem.surfaceId}`);
  }

  const resolution = resolveDashboardRendererAdapterForSurface(surface);

  return {
    routeId: `${navigationItem.navigationId}->${resolution.adapter.adapterId}`,
    navigationItem,
    surface,
    rendererAdapter: resolution.adapter,
    source: "dashboard_skeleton_navigation_binding",
    appTsxHardcodingAllowed: false,
    directEngineBindingAllowed: false,
  };
}

export function buildDashboardSkeletonNavigationRendererRouteBindingReadModel(): DashboardSkeletonNavigationRendererRouteBindingReadModel {
  const navigationReadModel = buildDashboardSkeletonNavigationBindingReadModel();

  const routes = navigationReadModel.sections
    .flatMap((section) => section.items)
    .map((navigationItem) => buildNavigationRendererRoute(navigationItem));

  return {
    source: "dashboard_skeleton_navigation_binding",
    navigationReadModel,
    routes,
    totalRoutes: routes.length,
    adapterBoundaryRoutes: routes.filter(
      (route) => route.surface.adapterBoundaryRequired,
    ).length,
    threeDRendererRoutes: routes.filter(
      (route) => route.rendererAdapter.adapterKind === "three_d_scene_renderer",
    ).length,
    simulationRendererRoutes: routes.filter(
      (route) =>
        route.rendererAdapter.adapterKind === "simulation_scene_renderer",
    ).length,
    memoryRendererRoutes: routes.filter(
      (route) => route.rendererAdapter.adapterKind === "memory_map_renderer",
    ).length,
    appTsxHardcodingAllowed: false,
    directEngineBindingAllowed: false,
  };
}

export function getDashboardSkeletonNavigationRendererRouteBySurfaceId(
  surfaceId: string,
): DashboardSkeletonNavigationRendererRoute | null {
  const navigationItem = getDashboardSkeletonNavigationItemBySurfaceId(surfaceId);

  if (!navigationItem) {
    return null;
  }

  return buildNavigationRendererRoute(navigationItem);
}

export function validateDashboardSkeletonNavigationRendererRouteBindingReadModel(
  readModel: DashboardSkeletonNavigationRendererRouteBindingReadModel =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel(),
): DashboardSkeletonNavigationRendererRouteValidation {
  const errors: string[] = [];
  const seenRouteIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.source !== "dashboard_skeleton_navigation_binding") {
    errors.push("source_must_be_dashboard_skeleton_navigation_binding");
  }

  if (readModel.totalRoutes !== readModel.navigationReadModel.totalItems) {
    errors.push("route_count_must_match_navigation_items");
  }

  for (const route of readModel.routes) {
    if (seenRouteIds.has(route.routeId)) {
      errors.push(`duplicate_routeId:${route.routeId}`);
    }

    seenRouteIds.add(route.routeId);

    if (seenSurfaceIds.has(route.surface.surfaceId)) {
      errors.push(`duplicate_surface_route:${route.surface.surfaceId}`);
    }

    seenSurfaceIds.add(route.surface.surfaceId);

    if (route.navigationItem.surfaceId !== route.surface.surfaceId) {
      errors.push(`navigation_surface_mismatch:${route.routeId}`);
    }

    if (
      !route.rendererAdapter.supportedRenderModes.includes(
        route.surface.renderMode,
      )
    ) {
      errors.push(`renderer_render_mode_mismatch:${route.routeId}`);
    }

    if (
      !route.rendererAdapter.supportedTargetZones.includes(
        route.surface.targetZone,
      )
    ) {
      errors.push(`renderer_target_zone_mismatch:${route.routeId}`);
    }

    if (route.rendererAdapter.directEngineBindingAllowed) {
      errors.push(`direct_engine_binding_forbidden:${route.routeId}`);
    }

    if (route.rendererAdapter.appTsxHardcodingAllowed) {
      errors.push(`app_tsx_hardcoding_forbidden:${route.routeId}`);
    }

    if (
      route.surface.adapterBoundaryRequired &&
      route.rendererAdapter.bindingPolicy !== "adapter_boundary_only"
    ) {
      errors.push(`adapter_boundary_policy_required:${route.routeId}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
