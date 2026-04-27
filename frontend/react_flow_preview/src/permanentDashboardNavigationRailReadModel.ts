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
  LeftDrawerSkeletonNavigationBadge,
  LeftDrawerSkeletonNavigationItem,
} from "./leftDrawerSkeletonNavigationExposure.js";
import {
  buildLeftDrawerSkeletonNavigationExposureReadModel,
  getLeftDrawerSkeletonNavigationExposureItemBySurfaceId,
} from "./leftDrawerSkeletonNavigationExposure.js";

export type PermanentDashboardNavigationRailTarget =
  "permanent_dashboard_navigation_rail";

export type PermanentDashboardNavigationRailSource =
  "left_drawer_skeleton_navigation_exposure";

export type PermanentDashboardNavigationRailDisplayMode =
  "persistent_left_rail";

export type PermanentDashboardNavigationRailItem = {
  railItemId: string;
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
  displayMode: PermanentDashboardNavigationRailDisplayMode;
  source: PermanentDashboardNavigationRailSource;
};

export type PermanentDashboardNavigationRailSection = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  items: readonly PermanentDashboardNavigationRailItem[];
};

export type PermanentDashboardNavigationRailReadModel = {
  target: PermanentDashboardNavigationRailTarget;
  source: PermanentDashboardNavigationRailSource;
  displayMode: PermanentDashboardNavigationRailDisplayMode;
  sections: readonly PermanentDashboardNavigationRailSection[];
  totalSections: number;
  totalItems: number;
  memoryItems: number;
  mobileItems: number;
  adapterBoundaryItems: number;
  threeDItems: number;
  simulationItems: number;
  persistent: true;
  appTsxHardcodingAllowed: false;
  drawerSemanticsAllowedForMainDashboardList: false;
};

export type PermanentDashboardNavigationRailValidation = {
  valid: boolean;
  errors: readonly string[];
};

function buildRailItem(
  item: LeftDrawerSkeletonNavigationItem,
): PermanentDashboardNavigationRailItem {
  return {
    railItemId: `rail:${item.navigationId}`,
    navigationId: item.navigationId,
    surfaceId: item.surfaceId,
    title: item.title,
    buttonGroup: item.buttonGroup,
    domain: item.domain,
    renderMode: item.renderMode,
    status: item.status,
    rendererAdapterKind: item.rendererAdapterKind,
    rendererAdapterId: item.rendererAdapterId,
    requiresApproval: item.requiresApproval,
    adapterBoundaryRequired: item.adapterBoundaryRequired,
    badges: item.badges,
    displayMode: "persistent_left_rail",
    source: "left_drawer_skeleton_navigation_exposure",
  };
}

export function buildPermanentDashboardNavigationRailReadModel(): PermanentDashboardNavigationRailReadModel {
  const exposure = buildLeftDrawerSkeletonNavigationExposureReadModel();

  const sections: PermanentDashboardNavigationRailSection[] =
    exposure.sections.map((section) => ({
      buttonGroup: section.buttonGroup,
      title: section.title,
      items: section.items.map((item) => buildRailItem(item)),
    }));

  const allItems = sections.flatMap((section) => section.items);

  return {
    target: "permanent_dashboard_navigation_rail",
    source: "left_drawer_skeleton_navigation_exposure",
    displayMode: "persistent_left_rail",
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
    persistent: true,
    appTsxHardcodingAllowed: false,
    drawerSemanticsAllowedForMainDashboardList: false,
  };
}

export function getPermanentDashboardNavigationRailItemBySurfaceId(
  surfaceId: string,
): PermanentDashboardNavigationRailItem | null {
  const exposureItem =
    getLeftDrawerSkeletonNavigationExposureItemBySurfaceId(surfaceId);

  if (!exposureItem) {
    return null;
  }

  return buildRailItem(exposureItem);
}

export function validatePermanentDashboardNavigationRailReadModel(
  readModel: PermanentDashboardNavigationRailReadModel =
    buildPermanentDashboardNavigationRailReadModel(),
): PermanentDashboardNavigationRailValidation {
  const errors: string[] = [];
  const seenRailItemIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.target !== "permanent_dashboard_navigation_rail") {
    errors.push("target_must_be_permanent_dashboard_navigation_rail");
  }

  if (readModel.displayMode !== "persistent_left_rail") {
    errors.push("display_mode_must_be_persistent_left_rail");
  }

  if (readModel.source !== "left_drawer_skeleton_navigation_exposure") {
    errors.push("source_must_be_left_drawer_skeleton_navigation_exposure");
  }

  if (!readModel.persistent) {
    errors.push("rail_must_be_persistent");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (readModel.drawerSemanticsAllowedForMainDashboardList) {
    errors.push("main_dashboard_list_must_not_use_drawer_semantics");
  }

  for (const section of readModel.sections) {
    if (section.items.length === 0) {
      errors.push(`empty_rail_section:${section.buttonGroup}`);
    }

    for (const item of section.items) {
      if (!item.railItemId.startsWith("rail:")) {
        errors.push(`rail_item_id_prefix_required:${item.surfaceId}`);
      }

      if (seenRailItemIds.has(item.railItemId)) {
        errors.push(`duplicate_railItemId:${item.railItemId}`);
      }

      seenRailItemIds.add(item.railItemId);

      if (seenSurfaceIds.has(item.surfaceId)) {
        errors.push(`duplicate_surfaceId:${item.surfaceId}`);
      }

      seenSurfaceIds.add(item.surfaceId);

      if (item.displayMode !== "persistent_left_rail") {
        errors.push(`item_display_mode_must_be_persistent_left_rail:${item.surfaceId}`);
      }

      if (item.domain === "memory_governance" && item.buttonGroup !== "memory") {
        errors.push(`memory_item_must_live_in_memory_group:${item.surfaceId}`);
      }

      if (item.domain === "mobile_companion" && item.buttonGroup !== "mobile") {
        errors.push(`mobile_item_must_live_in_mobile_group:${item.surfaceId}`);
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
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
