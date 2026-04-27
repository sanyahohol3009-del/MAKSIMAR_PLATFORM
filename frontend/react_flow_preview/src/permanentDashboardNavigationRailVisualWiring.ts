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
} from "./leftDrawerSkeletonNavigationExposure.js";
import type {
  PermanentDashboardNavigationRailItem,
  PermanentDashboardNavigationRailReadModel,
} from "./permanentDashboardNavigationRailReadModel.js";
import {
  buildPermanentDashboardNavigationRailReadModel,
  getPermanentDashboardNavigationRailItemBySurfaceId,
} from "./permanentDashboardNavigationRailReadModel.js";

export type PermanentDashboardNavigationRailVisualTarget =
  "permanent_left_dashboard_navigation_rail";

export type PermanentDashboardNavigationRailVisualSource =
  "permanent_dashboard_navigation_rail_read_model";

export type PermanentDashboardNavigationRailVisualPlacement =
  "left_permanent_rail";

export type PermanentDashboardNavigationRailVisualDensity =
  | "compact"
  | "expanded";

export type PermanentDashboardNavigationRailVisualItemKind =
  | "standard"
  | "memory"
  | "mobile"
  | "three_d"
  | "simulation"
  | "adapter_boundary";

export type PermanentDashboardNavigationRailVisualItem = {
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
  badges: readonly LeftDrawerSkeletonNavigationBadge[];
  visualKind: PermanentDashboardNavigationRailVisualItemKind;
  selected: boolean;
  disabled: boolean;
  requiresApproval: boolean;
  adapterBoundaryRequired: boolean;
};

export type PermanentDashboardNavigationRailVisualSection = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  items: readonly PermanentDashboardNavigationRailVisualItem[];
};

export type PermanentDashboardNavigationRailVisualWiringInput = {
  activeSurfaceId?: string;
  density?: PermanentDashboardNavigationRailVisualDensity;
};

export type PermanentDashboardNavigationRailVisualWiringReadModel = {
  target: PermanentDashboardNavigationRailVisualTarget;
  source: PermanentDashboardNavigationRailVisualSource;
  placement: PermanentDashboardNavigationRailVisualPlacement;
  density: PermanentDashboardNavigationRailVisualDensity;
  activeSurfaceId: string;
  sections: readonly PermanentDashboardNavigationRailVisualSection[];
  totalSections: number;
  totalItems: number;
  selectedItems: number;
  memoryItems: number;
  mobileItems: number;
  adapterBoundaryItems: number;
  threeDItems: number;
  simulationItems: number;
  persistent: true;
  overlay: false;
  centerViewportOverlapAllowed: false;
  drawerSemanticsAllowedForMainDashboardList: false;
  appTsxHardcodingAllowed: false;
};

export type PermanentDashboardNavigationRailVisualWiringValidation = {
  valid: boolean;
  errors: readonly string[];
};

const DEFAULT_ACTIVE_SURFACE_ID = "operator_home";

function resolveVisualKind(
  item: PermanentDashboardNavigationRailItem,
): PermanentDashboardNavigationRailVisualItemKind {
  if (item.rendererAdapterKind === "three_d_scene_renderer") {
    return "three_d";
  }

  if (item.rendererAdapterKind === "simulation_scene_renderer") {
    return "simulation";
  }

  if (item.domain === "memory_governance") {
    return "memory";
  }

  if (item.domain === "mobile_companion") {
    return "mobile";
  }

  if (item.adapterBoundaryRequired) {
    return "adapter_boundary";
  }

  return "standard";
}

function buildVisualItem(
  item: PermanentDashboardNavigationRailItem,
  activeSurfaceId: string,
): PermanentDashboardNavigationRailVisualItem {
  return {
    railItemId: item.railItemId,
    navigationId: item.navigationId,
    surfaceId: item.surfaceId,
    title: item.title,
    buttonGroup: item.buttonGroup,
    domain: item.domain,
    renderMode: item.renderMode,
    status: item.status,
    rendererAdapterKind: item.rendererAdapterKind,
    rendererAdapterId: item.rendererAdapterId,
    badges: item.badges,
    visualKind: resolveVisualKind(item),
    selected: item.surfaceId === activeSurfaceId,
    disabled: false,
    requiresApproval: item.requiresApproval,
    adapterBoundaryRequired: item.adapterBoundaryRequired,
  };
}

function resolveActiveSurfaceId(
  readModel: PermanentDashboardNavigationRailReadModel,
  input?: PermanentDashboardNavigationRailVisualWiringInput,
): string {
  const requestedSurfaceId = input?.activeSurfaceId ?? DEFAULT_ACTIVE_SURFACE_ID;
  const requestedItem =
    getPermanentDashboardNavigationRailItemBySurfaceId(requestedSurfaceId);

  if (requestedItem) {
    return requestedItem.surfaceId;
  }

  const fallbackItem = readModel.sections
    .flatMap((section) => section.items)
    .find((item) => item.surfaceId === DEFAULT_ACTIVE_SURFACE_ID);

  if (!fallbackItem) {
    throw new Error("default_dashboard_surface_not_found:operator_home");
  }

  return fallbackItem.surfaceId;
}

export function buildPermanentDashboardNavigationRailVisualWiringReadModel(
  input?: PermanentDashboardNavigationRailVisualWiringInput,
): PermanentDashboardNavigationRailVisualWiringReadModel {
  const railReadModel = buildPermanentDashboardNavigationRailReadModel();
  const activeSurfaceId = resolveActiveSurfaceId(railReadModel, input);

  const sections: PermanentDashboardNavigationRailVisualSection[] =
    railReadModel.sections.map((section) => ({
      buttonGroup: section.buttonGroup,
      title: section.title,
      items: section.items.map((item) => buildVisualItem(item, activeSurfaceId)),
    }));

  const allItems = sections.flatMap((section) => section.items);

  return {
    target: "permanent_left_dashboard_navigation_rail",
    source: "permanent_dashboard_navigation_rail_read_model",
    placement: "left_permanent_rail",
    density: input?.density ?? "compact",
    activeSurfaceId,
    sections,
    totalSections: sections.length,
    totalItems: allItems.length,
    selectedItems: allItems.filter((item) => item.selected).length,
    memoryItems: allItems.filter((item) => item.domain === "memory_governance")
      .length,
    mobileItems: allItems.filter((item) => item.domain === "mobile_companion")
      .length,
    adapterBoundaryItems: allItems.filter((item) => item.adapterBoundaryRequired)
      .length,
    threeDItems: allItems.filter((item) => item.visualKind === "three_d")
      .length,
    simulationItems: allItems.filter((item) => item.visualKind === "simulation")
      .length,
    persistent: true,
    overlay: false,
    centerViewportOverlapAllowed: false,
    drawerSemanticsAllowedForMainDashboardList: false,
    appTsxHardcodingAllowed: false,
  };
}

export function getPermanentDashboardNavigationRailVisualItemBySurfaceId(
  surfaceId: string,
): PermanentDashboardNavigationRailVisualItem | null {
  const readModel = buildPermanentDashboardNavigationRailVisualWiringReadModel({
    activeSurfaceId: surfaceId,
  });

  return (
    readModel.sections
      .flatMap((section) => section.items)
      .find((item) => item.surfaceId === surfaceId) ?? null
  );
}

export function validatePermanentDashboardNavigationRailVisualWiringReadModel(
  readModel: PermanentDashboardNavigationRailVisualWiringReadModel =
    buildPermanentDashboardNavigationRailVisualWiringReadModel(),
): PermanentDashboardNavigationRailVisualWiringValidation {
  const errors: string[] = [];
  const seenRailItemIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.target !== "permanent_left_dashboard_navigation_rail") {
    errors.push("target_must_be_permanent_left_dashboard_navigation_rail");
  }

  if (readModel.source !== "permanent_dashboard_navigation_rail_read_model") {
    errors.push("source_must_be_permanent_dashboard_navigation_rail_read_model");
  }

  if (readModel.placement !== "left_permanent_rail") {
    errors.push("placement_must_be_left_permanent_rail");
  }

  if (!readModel.persistent) {
    errors.push("rail_must_be_persistent");
  }

  if (readModel.overlay) {
    errors.push("rail_must_not_be_overlay");
  }

  if (readModel.centerViewportOverlapAllowed) {
    errors.push("rail_must_not_overlap_center_viewport");
  }

  if (readModel.drawerSemanticsAllowedForMainDashboardList) {
    errors.push("main_dashboard_list_must_not_use_drawer_semantics");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (readModel.selectedItems !== 1) {
    errors.push("exactly_one_selected_rail_item_required");
  }

  for (const section of readModel.sections) {
    if (section.items.length === 0) {
      errors.push(`empty_visual_rail_section:${section.buttonGroup}`);
    }

    for (const item of section.items) {
      if (seenRailItemIds.has(item.railItemId)) {
        errors.push(`duplicate_railItemId:${item.railItemId}`);
      }

      seenRailItemIds.add(item.railItemId);

      if (seenSurfaceIds.has(item.surfaceId)) {
        errors.push(`duplicate_surfaceId:${item.surfaceId}`);
      }

      seenSurfaceIds.add(item.surfaceId);

      if (item.domain === "memory_governance" && item.visualKind !== "memory") {
        errors.push(`memory_visual_kind_required:${item.surfaceId}`);
      }

      if (item.domain === "mobile_companion" && item.visualKind !== "mobile") {
        errors.push(`mobile_visual_kind_required:${item.surfaceId}`);
      }

      if (
        item.rendererAdapterKind === "three_d_scene_renderer" &&
        item.visualKind !== "three_d"
      ) {
        errors.push(`three_d_visual_kind_required:${item.surfaceId}`);
      }

      if (
        item.rendererAdapterKind === "simulation_scene_renderer" &&
        item.visualKind !== "simulation"
      ) {
        errors.push(`simulation_visual_kind_required:${item.surfaceId}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
