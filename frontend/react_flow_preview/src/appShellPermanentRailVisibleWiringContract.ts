import type {
  AppShellPermanentRailSlotInput,
} from "./appShellPermanentRailSlotContract.js";
import type {
  AppShellPermanentRailSlotWiringPreviewReadModel,
} from "./appShellPermanentRailSlotWiringPreview.js";
import {
  buildAppShellPermanentRailSlotWiringPreview,
  validateAppShellPermanentRailSlotWiringPreview,
} from "./appShellPermanentRailSlotWiringPreview.js";

export type AppShellPermanentRailVisibleWiringTarget =
  "appshell_permanent_rail_visible_wiring_contract";

export type AppShellPermanentRailVisibleWiringSource =
  "appshell_permanent_rail_slot_wiring_preview";

export type AppShellPermanentRailVisibleWiringHost = "AppShell";

export type AppShellPermanentRailVisibleWiringStatus =
  "visible_wiring_contract_ready";

export type AppShellPermanentRailVisibleWiringMode =
  "dedicated_shell_slot_only";

export type AppShellPermanentRailVisibleLayoutMode =
  "left_rail_center_viewport_shell_grid";

export type AppShellPermanentRailVisibleRailSlot = {
  slotId: "left_permanent_navigation_rail_slot";
  componentExportName: "PermanentDashboardNavigationRail";
  placement: "before_center_viewport";
  widthPx: number;
  persistent: true;
  overlay: false;
  drawer: false;
  mayOverlapCenterViewport: false;
};

export type AppShellPermanentRailVisibleCenterSlot = {
  slotId: "center_dashboard_viewport_slot";
  placement: "after_left_permanent_navigation_rail";
  widthPolicy: "remaining_shell_width";
  receivesActiveDashboardSurface: true;
  railMayOverlap: false;
};

export type AppShellPermanentRailVisibleContextualDrawerContract = {
  policy: "active_dashboard_only";
  leftDrawerPurpose: "functions_settings_tools";
  rightDrawerPurpose: "state_diagnostics_context";
  mayContainMainDashboardList: false;
};

export type AppShellPermanentRailVisibleTopCommunicationContract = {
  policy: "fullscreen_chat_separate";
  drawerPurpose: "jarvis_chat_surface";
  mayContainDashboardNavigation: false;
};

export type AppShellPermanentRailVisibleWiringContract = {
  target: AppShellPermanentRailVisibleWiringTarget;
  source: AppShellPermanentRailVisibleWiringSource;
  host: AppShellPermanentRailVisibleWiringHost;
  status: AppShellPermanentRailVisibleWiringStatus;
  wiringMode: AppShellPermanentRailVisibleWiringMode;
  layoutMode: AppShellPermanentRailVisibleLayoutMode;
  preview: AppShellPermanentRailSlotWiringPreviewReadModel;
  railSlot: AppShellPermanentRailVisibleRailSlot;
  centerViewportSlot: AppShellPermanentRailVisibleCenterSlot;
  contextualDrawers: AppShellPermanentRailVisibleContextualDrawerContract;
  topCommunication: AppShellPermanentRailVisibleTopCommunicationContract;
  visibleWiringAllowed: true;
  appTsxDirectButtonListAllowed: false;
  appTsxDirectRendererRouteLogicAllowed: false;
  appTsxDirectTaxonomyDuplicationAllowed: false;
  appTsxDirectClientGatingAllowed: false;
  appTsxDirectDrawerSemanticRewriteAllowed: false;
  dedicatedShellSlotRequired: true;
  readModelDriven: true;
};

export type AppShellPermanentRailVisibleWiringValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function buildAppShellPermanentRailVisibleWiringContract(
  input?: AppShellPermanentRailSlotInput,
): AppShellPermanentRailVisibleWiringContract {
  const previewInput: AppShellPermanentRailSlotInput = {
    ...(input?.activeSurfaceId !== undefined
      ? { activeSurfaceId: input.activeSurfaceId }
      : {}),
    ...(input?.density !== undefined ? { density: input.density } : {}),
  };

  const preview = buildAppShellPermanentRailSlotWiringPreview(previewInput);

  return {
    target: "appshell_permanent_rail_visible_wiring_contract",
    source: "appshell_permanent_rail_slot_wiring_preview",
    host: "AppShell",
    status: "visible_wiring_contract_ready",
    wiringMode: "dedicated_shell_slot_only",
    layoutMode: "left_rail_center_viewport_shell_grid",
    preview,
    railSlot: {
      slotId: "left_permanent_navigation_rail_slot",
      componentExportName: "PermanentDashboardNavigationRail",
      placement: "before_center_viewport",
      widthPx: preview.railSlot.widthPx,
      persistent: true,
      overlay: false,
      drawer: false,
      mayOverlapCenterViewport: false,
    },
    centerViewportSlot: {
      slotId: "center_dashboard_viewport_slot",
      placement: "after_left_permanent_navigation_rail",
      widthPolicy: "remaining_shell_width",
      receivesActiveDashboardSurface: true,
      railMayOverlap: false,
    },
    contextualDrawers: {
      policy: "active_dashboard_only",
      leftDrawerPurpose: "functions_settings_tools",
      rightDrawerPurpose: "state_diagnostics_context",
      mayContainMainDashboardList: false,
    },
    topCommunication: {
      policy: "fullscreen_chat_separate",
      drawerPurpose: "jarvis_chat_surface",
      mayContainDashboardNavigation: false,
    },
    visibleWiringAllowed: true,
    appTsxDirectButtonListAllowed: false,
    appTsxDirectRendererRouteLogicAllowed: false,
    appTsxDirectTaxonomyDuplicationAllowed: false,
    appTsxDirectClientGatingAllowed: false,
    appTsxDirectDrawerSemanticRewriteAllowed: false,
    dedicatedShellSlotRequired: true,
    readModelDriven: true,
  };
}

export function validateAppShellPermanentRailVisibleWiringContract(
  contract: AppShellPermanentRailVisibleWiringContract =
    buildAppShellPermanentRailVisibleWiringContract(),
): AppShellPermanentRailVisibleWiringValidation {
  const errors: string[] = [];

  if (contract.target !== "appshell_permanent_rail_visible_wiring_contract") {
    errors.push("target_must_be_appshell_permanent_rail_visible_wiring_contract");
  }

  if (contract.source !== "appshell_permanent_rail_slot_wiring_preview") {
    errors.push("source_must_be_appshell_permanent_rail_slot_wiring_preview");
  }

  if (contract.host !== "AppShell") {
    errors.push("host_must_be_AppShell");
  }

  if (contract.status !== "visible_wiring_contract_ready") {
    errors.push("status_must_be_visible_wiring_contract_ready");
  }

  if (contract.wiringMode !== "dedicated_shell_slot_only") {
    errors.push("wiring_mode_must_be_dedicated_shell_slot_only");
  }

  if (contract.layoutMode !== "left_rail_center_viewport_shell_grid") {
    errors.push("layout_mode_must_be_left_rail_center_viewport_shell_grid");
  }

  const previewValidation =
    validateAppShellPermanentRailSlotWiringPreview(contract.preview);

  if (!previewValidation.valid) {
    for (const error of previewValidation.errors) {
      errors.push(`preview_invalid:${error}`);
    }
  }

  if (contract.railSlot.slotId !== "left_permanent_navigation_rail_slot") {
    errors.push("rail_slot_id_must_be_left_permanent_navigation_rail_slot");
  }

  if (contract.railSlot.componentExportName !== "PermanentDashboardNavigationRail") {
    errors.push("rail_slot_component_must_be_PermanentDashboardNavigationRail");
  }

  if (contract.railSlot.placement !== "before_center_viewport") {
    errors.push("rail_slot_placement_must_be_before_center_viewport");
  }

  if (!contract.railSlot.persistent) {
    errors.push("rail_slot_must_be_persistent");
  }

  if (contract.railSlot.overlay) {
    errors.push("rail_slot_must_not_be_overlay");
  }

  if (contract.railSlot.drawer) {
    errors.push("rail_slot_must_not_be_drawer");
  }

  if (contract.railSlot.mayOverlapCenterViewport) {
    errors.push("rail_slot_must_not_overlap_center_viewport");
  }

  if (contract.centerViewportSlot.placement !== "after_left_permanent_navigation_rail") {
    errors.push("center_viewport_must_be_after_left_permanent_navigation_rail");
  }

  if (contract.centerViewportSlot.widthPolicy !== "remaining_shell_width") {
    errors.push("center_viewport_width_policy_must_be_remaining_shell_width");
  }

  if (!contract.centerViewportSlot.receivesActiveDashboardSurface) {
    errors.push("center_viewport_must_receive_active_dashboard_surface");
  }

  if (contract.centerViewportSlot.railMayOverlap) {
    errors.push("center_viewport_must_not_be_overlapped_by_rail");
  }

  if (contract.contextualDrawers.policy !== "active_dashboard_only") {
    errors.push("contextual_drawers_must_be_active_dashboard_only");
  }

  if (contract.contextualDrawers.mayContainMainDashboardList) {
    errors.push("contextual_drawers_must_not_contain_main_dashboard_list");
  }

  if (contract.topCommunication.policy !== "fullscreen_chat_separate") {
    errors.push("top_communication_must_remain_fullscreen_chat_separate");
  }

  if (contract.topCommunication.mayContainDashboardNavigation) {
    errors.push("top_communication_must_not_contain_dashboard_navigation");
  }

  if (!contract.visibleWiringAllowed) {
    errors.push("visible_wiring_must_be_allowed_by_contract");
  }

  if (contract.appTsxDirectButtonListAllowed) {
    errors.push("app_tsx_direct_button_list_forbidden");
  }

  if (contract.appTsxDirectRendererRouteLogicAllowed) {
    errors.push("app_tsx_direct_renderer_route_logic_forbidden");
  }

  if (contract.appTsxDirectTaxonomyDuplicationAllowed) {
    errors.push("app_tsx_direct_taxonomy_duplication_forbidden");
  }

  if (contract.appTsxDirectClientGatingAllowed) {
    errors.push("app_tsx_direct_client_gating_forbidden");
  }

  if (contract.appTsxDirectDrawerSemanticRewriteAllowed) {
    errors.push("app_tsx_direct_drawer_semantic_rewrite_forbidden");
  }

  if (!contract.dedicatedShellSlotRequired) {
    errors.push("dedicated_shell_slot_required");
  }

  if (!contract.readModelDriven) {
    errors.push("visible_wiring_must_be_read_model_driven");
  }

  if (contract.railSlot.widthPx !== contract.preview.railSlot.widthPx) {
    errors.push("rail_slot_width_must_match_preview");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
