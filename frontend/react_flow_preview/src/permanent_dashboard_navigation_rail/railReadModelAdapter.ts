import type {
  PermanentDashboardNavigationRailVisualItem,
  PermanentDashboardNavigationRailVisualWiringInput,
} from "../permanentDashboardNavigationRailVisualWiring.js";
import {
  buildPermanentDashboardNavigationRailVisualWiringReadModel,
} from "../permanentDashboardNavigationRailVisualWiring.js";
import type {
  PermanentDashboardNavigationRailShellItem,
  PermanentDashboardNavigationRailShellReadModel,
  PermanentDashboardNavigationRailShellSection,
  PermanentDashboardNavigationRailShellValidation,
} from "./types.js";

function buildShellItem(
  item: PermanentDashboardNavigationRailVisualItem,
): PermanentDashboardNavigationRailShellItem {
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
    visualKind: item.visualKind,
    selected: item.selected,
    disabled: item.disabled,
    requiresApproval: item.requiresApproval,
    adapterBoundaryRequired: item.adapterBoundaryRequired,
    badges: item.badges,
  };
}

export function buildPermanentDashboardNavigationRailShellReadModel(
  input?: PermanentDashboardNavigationRailVisualWiringInput,
): PermanentDashboardNavigationRailShellReadModel {
  const visualReadModel =
    buildPermanentDashboardNavigationRailVisualWiringReadModel(input);

  const sections: PermanentDashboardNavigationRailShellSection[] =
    visualReadModel.sections.map((section) => ({
      buttonGroup: section.buttonGroup,
      title: section.title,
      items: section.items.map((item) => buildShellItem(item)),
    }));

  return {
    target: "permanent_dashboard_navigation_rail_shell_component",
    source: "permanent_dashboard_navigation_rail_visual_wiring",
    placement: "left_permanent_rail",
    role: "dashboard_navigation",
    density: visualReadModel.density,
    activeSurfaceId: visualReadModel.activeSurfaceId,
    sections,
    totalSections: visualReadModel.totalSections,
    totalItems: visualReadModel.totalItems,
    selectedItems: visualReadModel.selectedItems,
    memoryItems: visualReadModel.memoryItems,
    mobileItems: visualReadModel.mobileItems,
    adapterBoundaryItems: visualReadModel.adapterBoundaryItems,
    threeDItems: visualReadModel.threeDItems,
    simulationItems: visualReadModel.simulationItems,
    persistent: true,
    overlay: false,
    centerViewportOverlapAllowed: false,
    drawerSemanticsAllowedForMainDashboardList: false,
    appTsxHardcodingAllowed: false,
  };
}

export function validatePermanentDashboardNavigationRailShellReadModel(
  readModel: PermanentDashboardNavigationRailShellReadModel =
    buildPermanentDashboardNavigationRailShellReadModel(),
): PermanentDashboardNavigationRailShellValidation {
  const errors: string[] = [];
  const seenRailItemIds = new Set<string>();
  const seenSurfaceIds = new Set<string>();

  if (readModel.target !== "permanent_dashboard_navigation_rail_shell_component") {
    errors.push("target_must_be_permanent_dashboard_navigation_rail_shell_component");
  }

  if (readModel.source !== "permanent_dashboard_navigation_rail_visual_wiring") {
    errors.push("source_must_be_permanent_dashboard_navigation_rail_visual_wiring");
  }

  if (readModel.placement !== "left_permanent_rail") {
    errors.push("placement_must_be_left_permanent_rail");
  }

  if (readModel.role !== "dashboard_navigation") {
    errors.push("role_must_be_dashboard_navigation");
  }

  if (!readModel.persistent) {
    errors.push("rail_shell_must_be_persistent");
  }

  if (readModel.overlay) {
    errors.push("rail_shell_must_not_be_overlay");
  }

  if (readModel.centerViewportOverlapAllowed) {
    errors.push("rail_shell_must_not_overlap_center_viewport");
  }

  if (readModel.drawerSemanticsAllowedForMainDashboardList) {
    errors.push("main_dashboard_list_must_not_use_drawer_semantics");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (readModel.selectedItems !== 1) {
    errors.push("exactly_one_selected_item_required");
  }

  for (const section of readModel.sections) {
    if (section.items.length === 0) {
      errors.push(`empty_shell_section:${section.buttonGroup}`);
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
