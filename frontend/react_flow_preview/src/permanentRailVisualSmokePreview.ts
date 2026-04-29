import type {
  PermanentDashboardNavigationRailVisualDensity,
} from "./permanentDashboardNavigationRailVisualWiring.js";
import type {
  PermanentDashboardNavigationRailShellReadModel,
} from "./permanentDashboardNavigationRailShellComponent.js";
import {
  buildPermanentDashboardNavigationRailShellReadModel,
  PermanentDashboardNavigationRail,
} from "./permanentDashboardNavigationRailShellComponent.js";
import type {
  PermanentRailVisibleLayoutVerificationReadModel,
} from "./permanentRailVisibleLayoutVerification.js";
import {
  buildPermanentRailVisibleLayoutVerification,
  validatePermanentRailVisibleLayoutVerification,
} from "./permanentRailVisibleLayoutVerification.js";
import {
  buildAppShellPermanentRailVisibleWiringContract,
} from "./appShellPermanentRailVisibleWiringContract.js";

export type PermanentRailVisualSmokePreviewTarget =
  "permanent_rail_visual_smoke_preview";

export type PermanentRailVisualSmokePreviewSource =
  "permanent_rail_visible_layout_verification";

export type PermanentRailVisualSmokePreviewStatus =
  "smoke_preview_ready";

export type PermanentRailVisualSmokePreviewInput = {
  activeSurfaceId?: string;
  density?: PermanentDashboardNavigationRailVisualDensity;
};

export type PermanentRailVisualSmokePreviewReadModel = {
  target: PermanentRailVisualSmokePreviewTarget;
  source: PermanentRailVisualSmokePreviewSource;
  status: PermanentRailVisualSmokePreviewStatus;
  componentExportName: "PermanentDashboardNavigationRail";
  componentAvailable: boolean;
  shellReadModel: PermanentDashboardNavigationRailShellReadModel;
  layoutVerification: PermanentRailVisibleLayoutVerificationReadModel;
  activeSurfaceId: string;
  density: PermanentDashboardNavigationRailVisualDensity;
  totalSections: number;
  totalItems: number;
  selectedItems: number;
  railWidthPx: number;
  railBeforeCenterViewport: boolean;
  railPersistent: true;
  railOverlay: false;
  railDrawer: false;
  centerViewportUsesRemainingWidth: boolean;
  contextualDrawersActiveDashboardOnly: boolean;
  topChatSeparate: boolean;
  manualDashboardButtonListAllowed: false;
  manualRendererRouteLogicAllowed: false;
  manualTaxonomyDuplicationAllowed: false;
};

export type PermanentRailVisualSmokePreviewValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function buildPermanentRailVisualSmokePreview(
  input?: PermanentRailVisualSmokePreviewInput,
): PermanentRailVisualSmokePreviewReadModel {
  const contract = buildAppShellPermanentRailVisibleWiringContract({
    ...(input?.activeSurfaceId !== undefined
      ? { activeSurfaceId: input.activeSurfaceId }
      : {}),
    ...(input?.density !== undefined ? { density: input.density } : {}),
  });

  const layoutVerification = buildPermanentRailVisibleLayoutVerification(contract);

  const shellReadModel = buildPermanentDashboardNavigationRailShellReadModel({
    activeSurfaceId:
      contract.preview.contract.integrationBoundary.shellReadModel.activeSurfaceId,
    density: contract.preview.contract.integrationBoundary.shellReadModel.density,
  });

  return {
    target: "permanent_rail_visual_smoke_preview",
    source: "permanent_rail_visible_layout_verification",
    status: "smoke_preview_ready",
    componentExportName: "PermanentDashboardNavigationRail",
    componentAvailable: typeof PermanentDashboardNavigationRail === "function",
    shellReadModel,
    layoutVerification,
    activeSurfaceId: shellReadModel.activeSurfaceId,
    density: shellReadModel.density,
    totalSections: shellReadModel.totalSections,
    totalItems: shellReadModel.totalItems,
    selectedItems: shellReadModel.selectedItems,
    railWidthPx: contract.railSlot.widthPx,
    railBeforeCenterViewport: layoutVerification.railBeforeCenterViewport,
    railPersistent: layoutVerification.railPersistent,
    railOverlay: layoutVerification.railOverlay,
    railDrawer: layoutVerification.railDrawer,
    centerViewportUsesRemainingWidth:
      layoutVerification.centerViewportUsesRemainingWidth,
    contextualDrawersActiveDashboardOnly:
      layoutVerification.contextualDrawersActiveDashboardOnly,
    topChatSeparate: layoutVerification.topChatSeparate,
    manualDashboardButtonListAllowed:
      layoutVerification.manualDashboardButtonListAllowed,
    manualRendererRouteLogicAllowed:
      layoutVerification.manualRendererRouteLogicAllowed,
    manualTaxonomyDuplicationAllowed:
      layoutVerification.manualTaxonomyDuplicationAllowed,
  };
}

export function validatePermanentRailVisualSmokePreview(
  preview: PermanentRailVisualSmokePreviewReadModel =
    buildPermanentRailVisualSmokePreview(),
): PermanentRailVisualSmokePreviewValidation {
  const errors: string[] = [];

  if (preview.target !== "permanent_rail_visual_smoke_preview") {
    errors.push("target_must_be_permanent_rail_visual_smoke_preview");
  }

  if (preview.source !== "permanent_rail_visible_layout_verification") {
    errors.push("source_must_be_permanent_rail_visible_layout_verification");
  }

  if (preview.status !== "smoke_preview_ready") {
    errors.push("status_must_be_smoke_preview_ready");
  }

  if (preview.componentExportName !== "PermanentDashboardNavigationRail") {
    errors.push("component_export_must_be_PermanentDashboardNavigationRail");
  }

  if (!preview.componentAvailable) {
    errors.push("PermanentDashboardNavigationRail_component_must_be_available");
  }

  const layoutValidation = validatePermanentRailVisibleLayoutVerification(
    preview.layoutVerification,
  );

  if (!layoutValidation.valid) {
    for (const error of layoutValidation.errors) {
      errors.push(`layout_verification_invalid:${error}`);
    }
  }

  if (preview.totalSections !== 19) {
    errors.push("total_sections_must_be_19");
  }

  if (preview.totalItems !== 38) {
    errors.push("total_items_must_be_38");
  }

  if (preview.selectedItems !== 1) {
    errors.push("selected_items_must_be_1");
  }

  if (!preview.railBeforeCenterViewport) {
    errors.push("rail_must_be_before_center_viewport");
  }

  if (!preview.railPersistent) {
    errors.push("rail_must_be_persistent");
  }

  if (preview.railOverlay) {
    errors.push("rail_must_not_be_overlay");
  }

  if (preview.railDrawer) {
    errors.push("rail_must_not_be_drawer");
  }

  if (!preview.centerViewportUsesRemainingWidth) {
    errors.push("center_viewport_must_use_remaining_width");
  }

  if (!preview.contextualDrawersActiveDashboardOnly) {
    errors.push("contextual_drawers_must_be_active_dashboard_only");
  }

  if (!preview.topChatSeparate) {
    errors.push("top_chat_must_remain_separate");
  }

  if (preview.manualDashboardButtonListAllowed) {
    errors.push("manual_dashboard_button_list_forbidden");
  }

  if (preview.manualRendererRouteLogicAllowed) {
    errors.push("manual_renderer_route_logic_forbidden");
  }

  if (preview.manualTaxonomyDuplicationAllowed) {
    errors.push("manual_taxonomy_duplication_forbidden");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
