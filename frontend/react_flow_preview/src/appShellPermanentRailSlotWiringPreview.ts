import type {
  AppShellPermanentRailSlotContract,
  AppShellPermanentRailSlotInput,
} from "./appShellPermanentRailSlotContract.js";
import {
  buildAppShellPermanentRailSlotContract,
  validateAppShellPermanentRailSlotContract,
} from "./appShellPermanentRailSlotContract.js";

export type AppShellPermanentRailSlotWiringPreviewTarget =
  "appshell_permanent_rail_slot_wiring_preview";

export type AppShellPermanentRailSlotWiringPreviewSource =
  "appshell_permanent_rail_slot_contract";

export type AppShellPermanentRailSlotWiringPreviewHost = "AppShell";

export type AppShellPermanentRailSlotWiringPreviewStatus =
  "preview_ready";

export type AppShellPermanentRailSlotWiringPreviewSlot = {
  slotId: "left_permanent_navigation_rail_slot";
  placement: "before_center_viewport";
  componentExportName: "PermanentDashboardNavigationRail";
  widthPx: number;
  persistent: true;
  overlay: false;
  drawer: false;
  centerViewportOverlapAllowed: false;
};

export type AppShellPermanentRailSlotWiringPreviewCenter = {
  slotId: "center_dashboard_viewport_slot";
  placement: "after_left_permanent_navigation_rail";
  widthPolicy: "remaining_shell_width";
  receivesActiveDashboardSurface: true;
  railMayOverlap: false;
};

export type AppShellPermanentRailSlotWiringPreviewContextualDrawers = {
  leftContextualDrawer: "active_dashboard_functions_settings_tools";
  rightContextualDrawer: "active_dashboard_state_diagnostics_context";
  policy: "active_dashboard_only";
  mayContainMainDashboardList: false;
};

export type AppShellPermanentRailSlotWiringPreviewTopCommunication = {
  topCommunicationDrawer: "fullscreen_jarvis_chat";
  policy: "fullscreen_chat_separate";
  mayContainDashboardNavigation: false;
};

export type AppShellPermanentRailSlotWiringPreviewReadModel = {
  target: AppShellPermanentRailSlotWiringPreviewTarget;
  source: AppShellPermanentRailSlotWiringPreviewSource;
  host: AppShellPermanentRailSlotWiringPreviewHost;
  status: AppShellPermanentRailSlotWiringPreviewStatus;
  contract: AppShellPermanentRailSlotContract;
  railSlot: AppShellPermanentRailSlotWiringPreviewSlot;
  centerViewportSlot: AppShellPermanentRailSlotWiringPreviewCenter;
  contextualDrawers: AppShellPermanentRailSlotWiringPreviewContextualDrawers;
  topCommunication: AppShellPermanentRailSlotWiringPreviewTopCommunication;
  appTsxModificationAllowed: false;
  appTsxHardcodingAllowed: false;
  manualDashboardButtonListAllowed: false;
  manualRendererRouteLogicAllowed: false;
  manualTaxonomyDuplicationAllowed: false;
};

export type AppShellPermanentRailSlotWiringPreviewValidation = {
  valid: boolean;
  errors: readonly string[];
};

function resolveRailWidth(contract: AppShellPermanentRailSlotContract): number {
  return contract.integrationBoundary.shellReadModel.density === "expanded"
    ? contract.expandedWidthPx
    : contract.compactWidthPx;
}

export function buildAppShellPermanentRailSlotWiringPreview(
  input?: AppShellPermanentRailSlotInput,
): AppShellPermanentRailSlotWiringPreviewReadModel {
  const contract = buildAppShellPermanentRailSlotContract(input);

  return {
    target: "appshell_permanent_rail_slot_wiring_preview",
    source: "appshell_permanent_rail_slot_contract",
    host: "AppShell",
    status: "preview_ready",
    contract,
    railSlot: {
      slotId: "left_permanent_navigation_rail_slot",
      placement: "before_center_viewport",
      componentExportName: "PermanentDashboardNavigationRail",
      widthPx: resolveRailWidth(contract),
      persistent: true,
      overlay: false,
      drawer: false,
      centerViewportOverlapAllowed: false,
    },
    centerViewportSlot: {
      slotId: "center_dashboard_viewport_slot",
      placement: "after_left_permanent_navigation_rail",
      widthPolicy: "remaining_shell_width",
      receivesActiveDashboardSurface: true,
      railMayOverlap: false,
    },
    contextualDrawers: {
      leftContextualDrawer: "active_dashboard_functions_settings_tools",
      rightContextualDrawer: "active_dashboard_state_diagnostics_context",
      policy: "active_dashboard_only",
      mayContainMainDashboardList: false,
    },
    topCommunication: {
      topCommunicationDrawer: "fullscreen_jarvis_chat",
      policy: "fullscreen_chat_separate",
      mayContainDashboardNavigation: false,
    },
    appTsxModificationAllowed: false,
    appTsxHardcodingAllowed: false,
    manualDashboardButtonListAllowed: false,
    manualRendererRouteLogicAllowed: false,
    manualTaxonomyDuplicationAllowed: false,
  };
}

export function validateAppShellPermanentRailSlotWiringPreview(
  preview: AppShellPermanentRailSlotWiringPreviewReadModel =
    buildAppShellPermanentRailSlotWiringPreview(),
): AppShellPermanentRailSlotWiringPreviewValidation {
  const errors: string[] = [];

  if (preview.target !== "appshell_permanent_rail_slot_wiring_preview") {
    errors.push("target_must_be_appshell_permanent_rail_slot_wiring_preview");
  }

  if (preview.source !== "appshell_permanent_rail_slot_contract") {
    errors.push("source_must_be_appshell_permanent_rail_slot_contract");
  }

  if (preview.host !== "AppShell") {
    errors.push("host_must_be_AppShell");
  }

  if (preview.status !== "preview_ready") {
    errors.push("status_must_be_preview_ready");
  }

  const contractValidation = validateAppShellPermanentRailSlotContract(
    preview.contract,
  );

  if (!contractValidation.valid) {
    for (const error of contractValidation.errors) {
      errors.push(`slot_contract_invalid:${error}`);
    }
  }

  if (preview.railSlot.slotId !== "left_permanent_navigation_rail_slot") {
    errors.push("rail_slot_id_must_be_left_permanent_navigation_rail_slot");
  }

  if (preview.railSlot.placement !== "before_center_viewport") {
    errors.push("rail_slot_placement_must_be_before_center_viewport");
  }

  if (preview.railSlot.componentExportName !== "PermanentDashboardNavigationRail") {
    errors.push("rail_slot_component_must_be_PermanentDashboardNavigationRail");
  }

  if (!preview.railSlot.persistent) {
    errors.push("rail_slot_must_be_persistent");
  }

  if (preview.railSlot.overlay) {
    errors.push("rail_slot_must_not_be_overlay");
  }

  if (preview.railSlot.drawer) {
    errors.push("rail_slot_must_not_be_drawer");
  }

  if (preview.railSlot.centerViewportOverlapAllowed) {
    errors.push("rail_slot_must_not_overlap_center_viewport");
  }

  if (
    preview.centerViewportSlot.placement !==
    "after_left_permanent_navigation_rail"
  ) {
    errors.push("center_viewport_must_be_after_left_permanent_navigation_rail");
  }

  if (preview.centerViewportSlot.widthPolicy !== "remaining_shell_width") {
    errors.push("center_viewport_width_policy_must_be_remaining_shell_width");
  }

  if (!preview.centerViewportSlot.receivesActiveDashboardSurface) {
    errors.push("center_viewport_must_receive_active_dashboard_surface");
  }

  if (preview.centerViewportSlot.railMayOverlap) {
    errors.push("center_viewport_must_not_be_overlapped_by_rail");
  }

  if (preview.contextualDrawers.policy !== "active_dashboard_only") {
    errors.push("contextual_drawers_must_be_active_dashboard_only");
  }

  if (preview.contextualDrawers.mayContainMainDashboardList) {
    errors.push("contextual_drawers_must_not_contain_main_dashboard_list");
  }

  if (preview.topCommunication.policy !== "fullscreen_chat_separate") {
    errors.push("top_communication_must_remain_fullscreen_chat_separate");
  }

  if (preview.topCommunication.mayContainDashboardNavigation) {
    errors.push("top_communication_must_not_contain_dashboard_navigation");
  }

  if (preview.appTsxModificationAllowed) {
    errors.push("app_tsx_modification_forbidden_in_preview_step");
  }

  if (preview.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
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
