import type {
  PermanentDashboardNavigationRailVisualDensity,
} from "./permanentDashboardNavigationRailVisualWiring.js";
import type {
  PermanentDashboardNavigationRailShellIntegrationBoundary,
  PermanentDashboardNavigationRailShellIntegrationInput,
} from "./permanentDashboardNavigationRailShellIntegrationBoundary.js";
import {
  buildPermanentDashboardNavigationRailShellIntegrationBoundary,
  validatePermanentDashboardNavigationRailShellIntegrationBoundary,
} from "./permanentDashboardNavigationRailShellIntegrationBoundary.js";

export type AppShellPermanentRailSlotTarget =
  "appshell_permanent_rail_slot_contract";

export type AppShellPermanentRailSlotSource =
  "permanent_dashboard_navigation_rail_shell_integration_boundary";

export type AppShellPermanentRailSlotHost = "AppShell";

export type AppShellPermanentRailSlotId =
  "left_permanent_navigation_rail_slot";

export type AppShellPermanentRailSlotPlacement =
  "before_center_viewport";

export type AppShellPermanentRailCenterPolicy =
  "reserve_width_before_center_viewport";

export type AppShellPermanentRailOverlayPolicy =
  "not_overlay_not_drawer";

export type AppShellPermanentRailContextualDrawerPolicy =
  "contextual_drawers_remain_active_dashboard_only";

export type AppShellPermanentRailTopCommunicationPolicy =
  "top_chat_remains_fullscreen_separate";

export type AppShellPermanentRailSlotInput = {
  activeSurfaceId?: string;
  density?: PermanentDashboardNavigationRailVisualDensity;
};

export type AppShellPermanentRailSlotContract = {
  target: AppShellPermanentRailSlotTarget;
  source: AppShellPermanentRailSlotSource;
  host: AppShellPermanentRailSlotHost;
  slotId: AppShellPermanentRailSlotId;
  placement: AppShellPermanentRailSlotPlacement;
  centerPolicy: AppShellPermanentRailCenterPolicy;
  overlayPolicy: AppShellPermanentRailOverlayPolicy;
  contextualDrawerPolicy: AppShellPermanentRailContextualDrawerPolicy;
  topCommunicationPolicy: AppShellPermanentRailTopCommunicationPolicy;
  integrationBoundary: PermanentDashboardNavigationRailShellIntegrationBoundary;
  componentExportName: "PermanentDashboardNavigationRail";
  compactWidthPx: 104;
  expandedWidthPx: 284;
  persistent: true;
  overlay: false;
  drawer: false;
  centerViewportOverlapAllowed: false;
  appTsxHardcodingAllowed: false;
  directDashboardButtonHardcodingAllowed: false;
  manualDashboardTaxonomyAllowed: false;
  manualRendererRouteLogicAllowed: false;
};

export type AppShellPermanentRailSlotValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function buildAppShellPermanentRailSlotContract(
  input?: AppShellPermanentRailSlotInput,
): AppShellPermanentRailSlotContract {
  const integrationInput: PermanentDashboardNavigationRailShellIntegrationInput =
    {
      ...(input?.activeSurfaceId !== undefined
        ? { activeSurfaceId: input.activeSurfaceId }
        : {}),
      ...(input?.density !== undefined ? { density: input.density } : {}),
    };

  const integrationBoundary =
    buildPermanentDashboardNavigationRailShellIntegrationBoundary(
      integrationInput,
    );

  return {
    target: "appshell_permanent_rail_slot_contract",
    source: "permanent_dashboard_navigation_rail_shell_integration_boundary",
    host: "AppShell",
    slotId: "left_permanent_navigation_rail_slot",
    placement: "before_center_viewport",
    centerPolicy: "reserve_width_before_center_viewport",
    overlayPolicy: "not_overlay_not_drawer",
    contextualDrawerPolicy: "contextual_drawers_remain_active_dashboard_only",
    topCommunicationPolicy: "top_chat_remains_fullscreen_separate",
    integrationBoundary,
    componentExportName: "PermanentDashboardNavigationRail",
    compactWidthPx: integrationBoundary.layoutContract.compactWidthPx,
    expandedWidthPx: integrationBoundary.layoutContract.expandedWidthPx,
    persistent: true,
    overlay: false,
    drawer: false,
    centerViewportOverlapAllowed: false,
    appTsxHardcodingAllowed: false,
    directDashboardButtonHardcodingAllowed: false,
    manualDashboardTaxonomyAllowed: false,
    manualRendererRouteLogicAllowed: false,
  };
}

export function validateAppShellPermanentRailSlotContract(
  contract: AppShellPermanentRailSlotContract =
    buildAppShellPermanentRailSlotContract(),
): AppShellPermanentRailSlotValidation {
  const errors: string[] = [];

  if (contract.target !== "appshell_permanent_rail_slot_contract") {
    errors.push("target_must_be_appshell_permanent_rail_slot_contract");
  }

  if (
    contract.source !==
    "permanent_dashboard_navigation_rail_shell_integration_boundary"
  ) {
    errors.push("source_must_be_permanent_dashboard_navigation_rail_shell_integration_boundary");
  }

  if (contract.host !== "AppShell") {
    errors.push("host_must_be_AppShell");
  }

  if (contract.slotId !== "left_permanent_navigation_rail_slot") {
    errors.push("slot_id_must_be_left_permanent_navigation_rail_slot");
  }

  if (contract.placement !== "before_center_viewport") {
    errors.push("placement_must_be_before_center_viewport");
  }

  if (contract.centerPolicy !== "reserve_width_before_center_viewport") {
    errors.push("center_policy_must_reserve_width_before_center_viewport");
  }

  if (contract.overlayPolicy !== "not_overlay_not_drawer") {
    errors.push("overlay_policy_must_be_not_overlay_not_drawer");
  }

  if (
    contract.contextualDrawerPolicy !==
    "contextual_drawers_remain_active_dashboard_only"
  ) {
    errors.push("contextual_drawer_policy_must_remain_active_dashboard_only");
  }

  if (
    contract.topCommunicationPolicy !==
    "top_chat_remains_fullscreen_separate"
  ) {
    errors.push("top_chat_policy_must_remain_fullscreen_separate");
  }

  if (contract.componentExportName !== "PermanentDashboardNavigationRail") {
    errors.push("component_export_must_be_PermanentDashboardNavigationRail");
  }

  if (contract.compactWidthPx !== 104) {
    errors.push("compact_width_must_be_104");
  }

  if (contract.expandedWidthPx !== 284) {
    errors.push("expanded_width_must_be_284");
  }

  if (!contract.persistent) {
    errors.push("rail_slot_must_be_persistent");
  }

  if (contract.overlay) {
    errors.push("rail_slot_must_not_be_overlay");
  }

  if (contract.drawer) {
    errors.push("rail_slot_must_not_be_drawer");
  }

  if (contract.centerViewportOverlapAllowed) {
    errors.push("rail_slot_must_not_overlap_center_viewport");
  }

  if (contract.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (contract.directDashboardButtonHardcodingAllowed) {
    errors.push("direct_dashboard_button_hardcoding_forbidden");
  }

  if (contract.manualDashboardTaxonomyAllowed) {
    errors.push("manual_dashboard_taxonomy_forbidden");
  }

  if (contract.manualRendererRouteLogicAllowed) {
    errors.push("manual_renderer_route_logic_forbidden");
  }

  const boundaryValidation =
    validatePermanentDashboardNavigationRailShellIntegrationBoundary(
      contract.integrationBoundary,
    );

  if (!boundaryValidation.valid) {
    for (const error of boundaryValidation.errors) {
      errors.push(`integration_boundary_invalid:${error}`);
    }
  }

  if (contract.integrationBoundary.slot !== contract.slotId) {
    errors.push("integration_boundary_slot_mismatch");
  }

  if (
    contract.integrationBoundary.componentExportName !==
    contract.componentExportName
  ) {
    errors.push("integration_boundary_component_export_mismatch");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
