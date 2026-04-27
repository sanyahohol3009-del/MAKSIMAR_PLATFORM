import type {
  DashboardSkeletonButtonGroup,
  DashboardSkeletonDomain,
  DashboardSkeletonRenderMode,
  DashboardSkeletonSurfaceStatus,
} from "./dashboardSkeletonSurfaceTaxonomy.js";
import type {
  DashboardRendererAdapterKind,
} from "./dashboardRendererAdapterBoundary.js";
import type {
  DashboardSkeletonNavigationRendererRoute,
} from "./dashboardSkeletonNavigationRendererRouteBinding.js";
import {
  buildDashboardSkeletonNavigationRendererRouteBindingReadModel,
  getDashboardSkeletonNavigationRendererRouteBySurfaceId,
} from "./dashboardSkeletonNavigationRendererRouteBinding.js";

export type LeftDrawerSkeletonNavigationExposureSource =
  "dashboard_skeleton_navigation_renderer_route_binding";

export type LeftDrawerSkeletonNavigationExposureTarget =
  "left_dashboard_drawer";

export type LeftDrawerSkeletonNavigationBadge =
  | "implemented"
  | "reserved"
  | "approval_required"
  | "adapter_boundary"
  | "memory"
  | "mobile"
  | "three_d"
  | "simulation";

export type LeftDrawerSkeletonNavigationItem = {
  navigationId: string;
  surfaceId: string;
  title: string;
  buttonGroup: DashboardSkeletonButtonGroup;
  domain: DashboardSkeletonDomain;
  renderMode: DashboardSkeletonRenderMode;
  status: DashboardSkeletonSurfaceStatus;
  rendererAdapterKind: DashboardRendererAdapterKind;
  rendererAdapterId: string;
  requiresApproval: boolean;
  adapterBoundaryRequired: boolean;
  badges: readonly LeftDrawerSkeletonNavigationBadge[];
  source: LeftDrawerSkeletonNavigationExposureSource;
};

export type LeftDrawerSkeletonNavigationSection = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  items: readonly LeftDrawerSkeletonNavigationItem[];
};

export type LeftDrawerSkeletonNavigationExposureReadModel = {
  target: LeftDrawerSkeletonNavigationExposureTarget;
  source: LeftDrawerSkeletonNavigationExposureSource;
  sections: readonly LeftDrawerSkeletonNavigationSection[];
  totalSections: number;
  totalItems: number;
  memoryItems: number;
  mobileItems: number;
  adapterBoundaryItems: number;
  threeDItems: number;
  simulationItems: number;
  appTsxHardcodingAllowed: false;
};

export type LeftDrawerSkeletonNavigationExposureValidation = {
  valid: boolean;
  errors: readonly string[];
};

function buildBadges(
  route: DashboardSkeletonNavigationRendererRoute,
): readonly LeftDrawerSkeletonNavigationBadge[] {
  const badges: LeftDrawerSkeletonNavigationBadge[] = [];

  badges.push(route.surface.status);

  if (route.surface.requiresApproval) {
    badges.push("approval_required");
  }

  if (route.surface.adapterBoundaryRequired) {
    badges.push("adapter_boundary");
  }

  if (route.surface.domain === "memory_governance") {
    badges.push("memory");
  }

  if (route.surface.domain === "mobile_companion") {
    badges.push("mobile");
  }

  if (route.rendererAdapter.adapterKind === "three_d_scene_renderer") {
    badges.push("three_d");
  }

  if (route.rendererAdapter.adapterKind === "simulation_scene_renderer") {
    badges.push("simulation");
  }

  return badges;
}

function buildExposureItem(
  route: DashboardSkeletonNavigationRendererRoute,
): LeftDrawerSkeletonNavigationItem {
  return {
    navigationId: route.navigationItem.navigationId,
    surfaceId: route.surface.surfaceId,
    title: route.surface.title,
    buttonGroup: route.surface.buttonGroup,
    domain: route.surface.domain,
    renderMode: route.surface.renderMode,
    status: route.surface.status,
    rendererAdapterKind: route.rendererAdapter.adapterKind,
    rendererAdapterId: route.rendererAdapter.adapterId,
    requiresApproval: route.surface.requiresApproval,
    adapterBoundaryRequired: route.surface.adapterBoundaryRequired,
    badges: buildBadges(route),
    source: "dashboard_skeleton_navigation_renderer_route_binding",
  };
}

export function buildLeftDrawerSkeletonNavigationExposureReadModel(): LeftDrawerSkeletonNavigationExposureReadModel {
  const routeReadModel =
    buildDashboardSkeletonNavigationRendererRouteBindingReadModel();

  const sections: LeftDrawerSkeletonNavigationSection[] =
    routeReadModel.navigationReadModel.sections.map((section) => {
      const items = section.items.map((navigationItem) => {
        const route = getDashboardSkeletonNavigationRendererRouteBySurfaceId(
          navigationItem.surfaceId,
        );

        if (!route) {
          throw new Error(`navigation_renderer_route_not_found:${navigationItem.surfaceId}`);
        }

        return buildExposureItem(route);
      });

      return {
        buttonGroup: section.buttonGroup,
        title: section.title,
        items,
      };
    });

  const allItems = sections.flatMap((section) => section.items);

  return {
    target: "left_dashboard_drawer",
    source: "dashboard_skeleton_navigation_renderer_route_binding",
    sections,
    totalSections: sections.length,
    totalItems: allItems.length,
    memoryItems: allItems.filter((item) => item.domain === "memory_governance")
      .length,
    mobileItems: allItems.filter((item) => item.domain === "mobile_companion")
      .length,
    adapterBoundaryItems: allItems.filter((item) => item.adapterBoundaryRequired)
      .length,
    threeDItems: allItems.filter(
      (item) => item.rendererAdapterKind === "three_d_scene_renderer",
    ).length,
    simulationItems: allItems.filter(
      (item) => item.rendererAdapterKind === "simulation_scene_renderer",
    ).length,
    appTsxHardcodingAllowed: false,
  };
}

export function getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(
  surfaceId: string,
): LeftDrawerSkeletonNavigationItem | null {
  const readModel = buildLeftDrawerSkeletonNavigationExposureReadModel();

  return (
    readModel.sections
      .flatMap((section) => section.items)
      .find((item) => item.surfaceId === surfaceId) ?? null
  );
}

export function validateLeftDrawerSkeletonNavigationExposureReadModel(
  readModel: LeftDrawerSkeletonNavigationExposureReadModel =
    buildLeftDrawerSkeletonNavigationExposureReadModel(),
): LeftDrawerSkeletonNavigationExposureValidation {
  const errors: string[] = [];
  const seenNavigationIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.target !== "left_dashboard_drawer") {
    errors.push("target_must_be_left_dashboard_drawer");
  }

  if (readModel.source !== "dashboard_skeleton_navigation_renderer_route_binding") {
    errors.push("source_must_be_dashboard_skeleton_navigation_renderer_route_binding");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  for (const section of readModel.sections) {
    if (section.items.length === 0) {
      errors.push(`empty_left_drawer_section:${section.buttonGroup}`);
    }

    for (const item of section.items) {
      if (seenNavigationIds.has(item.navigationId)) {
        errors.push(`duplicate_navigationId:${item.navigationId}`);
      }

      seenNavigationIds.add(item.navigationId);

      if (seenSurfaceIds.has(item.surfaceId)) {
        errors.push(`duplicate_surfaceId:${item.surfaceId}`);
      }

      seenSurfaceIds.add(item.surfaceId);

      if (item.domain === "memory_governance" && !item.badges.includes("memory")) {
        errors.push(`memory_badge_required:${item.surfaceId}`);
      }

      if (item.domain === "mobile_companion" && !item.badges.includes("mobile")) {
        errors.push(`mobile_badge_required:${item.surfaceId}`);
      }

      if (
        item.rendererAdapterKind === "three_d_scene_renderer" &&
        !item.badges.includes("three_d")
      ) {
        errors.push(`three_d_badge_required:${item.surfaceId}`);
      }

      if (
        item.rendererAdapterKind === "simulation_scene_renderer" &&
        !item.badges.includes("simulation")
      ) {
        errors.push(`simulation_badge_required:${item.surfaceId}`);
      }

      if (
        item.adapterBoundaryRequired &&
        !item.badges.includes("adapter_boundary")
      ) {
        errors.push(`adapter_boundary_badge_required:${item.surfaceId}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
