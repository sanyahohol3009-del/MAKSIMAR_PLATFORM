import type {
  DashboardSkeletonButtonGroup,
  DashboardSkeletonDomain,
  DashboardSkeletonRenderMode,
  DashboardSkeletonSurfaceStatus,
} from "./dashboardSkeletonSurfaceTaxonomy.js";
import {
  getDashboardSkeletonSurfaceById,
  groupDashboardSkeletonSurfacesByButtonGroup,
} from "./dashboardSkeletonSurfaceTaxonomy.js";
import type { DashboardSurfaceTargetZone } from "./dashboardModuleRegistrationContract.js";

export type DashboardSkeletonNavigationBindingSource =
  "dashboard_skeleton_surface_taxonomy";

export type DashboardSkeletonNavigationTargetShell =
  "left_dashboard_drawer";

export type DashboardSkeletonNavigationItem = {
  navigationId: string;
  surfaceId: string;
  title: string;
  buttonGroup: DashboardSkeletonButtonGroup;
  domain: DashboardSkeletonDomain;
  targetZone: DashboardSurfaceTargetZone;
  renderMode: DashboardSkeletonRenderMode;
  status: DashboardSkeletonSurfaceStatus;
  clientSelectable: boolean;
  requiresApproval: boolean;
  adapterBoundaryRequired: boolean;
  bindingSource: DashboardSkeletonNavigationBindingSource;
};

export type DashboardSkeletonNavigationSection = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  items: readonly DashboardSkeletonNavigationItem[];
};

export type DashboardSkeletonNavigationBindingReadModel = {
  targetShell: DashboardSkeletonNavigationTargetShell;
  bindingSource: DashboardSkeletonNavigationBindingSource;
  sections: readonly DashboardSkeletonNavigationSection[];
  totalSections: number;
  totalItems: number;
  implementedItems: number;
  reservedItems: number;
  adapterBoundaryItems: number;
  memoryItems: number;
  mobileItems: number;
  appTsxHardcodingAllowed: false;
};

export type DashboardSkeletonNavigationBindingValidation = {
  valid: boolean;
  errors: readonly string[];
};

function buildNavigationItem(
  section: DashboardSkeletonNavigationSection,
  surfaceId: string,
): DashboardSkeletonNavigationItem {
  const surface = getDashboardSkeletonSurfaceById(surfaceId);

  if (!surface) {
    throw new Error(`dashboard_surface_not_found:${surfaceId}`);
  }

  return {
    navigationId: `${section.buttonGroup}:${surface.surfaceId}`,
    surfaceId: surface.surfaceId,
    title: surface.title,
    buttonGroup: surface.buttonGroup,
    domain: surface.domain,
    targetZone: surface.targetZone,
    renderMode: surface.renderMode,
    status: surface.status,
    clientSelectable: surface.clientSelectable,
    requiresApproval: surface.requiresApproval,
    adapterBoundaryRequired: surface.adapterBoundaryRequired,
    bindingSource: "dashboard_skeleton_surface_taxonomy",
  };
}

export function buildDashboardSkeletonNavigationBindingReadModel(): DashboardSkeletonNavigationBindingReadModel {
  const sections: DashboardSkeletonNavigationSection[] =
    groupDashboardSkeletonSurfacesByButtonGroup().map((group) => {
      const sectionShell: DashboardSkeletonNavigationSection = {
        buttonGroup: group.buttonGroup,
        title: group.title,
        items: [],
      };

      const items = group.surfaces.map((surface) =>
        buildNavigationItem(sectionShell, surface.surfaceId),
      );

      return {
        ...sectionShell,
        items,
      };
    });

  const allItems = sections.flatMap((section) => section.items);

  return {
    targetShell: "left_dashboard_drawer",
    bindingSource: "dashboard_skeleton_surface_taxonomy",
    sections,
    totalSections: sections.length,
    totalItems: allItems.length,
    implementedItems: allItems.filter((item) => item.status === "implemented")
      .length,
    reservedItems: allItems.filter((item) => item.status === "reserved").length,
    adapterBoundaryItems: allItems.filter((item) => item.adapterBoundaryRequired)
      .length,
    memoryItems: allItems.filter((item) => item.domain === "memory_governance")
      .length,
    mobileItems: allItems.filter((item) => item.domain === "mobile_companion")
      .length,
    appTsxHardcodingAllowed: false,
  };
}

export function getDashboardSkeletonNavigationItemBySurfaceId(
  surfaceId: string,
): DashboardSkeletonNavigationItem | null {
  const readModel = buildDashboardSkeletonNavigationBindingReadModel();

  return (
    readModel.sections
      .flatMap((section) => section.items)
      .find((item) => item.surfaceId === surfaceId) ?? null
  );
}

export function validateDashboardSkeletonNavigationBindingReadModel(
  readModel: DashboardSkeletonNavigationBindingReadModel =
    buildDashboardSkeletonNavigationBindingReadModel(),
): DashboardSkeletonNavigationBindingValidation {
  const errors: string[] = [];
  const seenNavigationIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (readModel.targetShell !== "left_dashboard_drawer") {
    errors.push("target_shell_must_be_left_dashboard_drawer");
  }

  if (readModel.bindingSource !== "dashboard_skeleton_surface_taxonomy") {
    errors.push("binding_source_must_be_dashboard_skeleton_surface_taxonomy");
  }

  for (const section of readModel.sections) {
    if (section.items.length === 0) {
      errors.push(`empty_navigation_section:${section.buttonGroup}`);
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

      if (!item.clientSelectable) {
        errors.push(`navigation_item_not_client_selectable:${item.surfaceId}`);
      }

      if (item.domain === "mobile_companion" && item.buttonGroup !== "mobile") {
        errors.push(`mobile_item_must_live_in_mobile_group:${item.surfaceId}`);
      }

      if (item.domain === "memory_governance" && item.buttonGroup !== "memory") {
        errors.push(`memory_item_must_live_in_memory_group:${item.surfaceId}`);
      }

      if (
        item.adapterBoundaryRequired &&
        item.renderMode !== "three_d_scene_adapter" &&
        item.renderMode !== "simulation_scene_adapter"
      ) {
        errors.push(`unexpected_adapter_boundary_item:${item.surfaceId}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
