import type {
  PermanentDashboardNavigationRailVisualDensity,
} from "./permanentDashboardNavigationRailVisualWiring.js";
import type {
  PermanentDashboardNavigationRailShellReadModel,
} from "./permanentDashboardNavigationRailShellComponent.js";
import {
  buildPermanentDashboardNavigationRailShellReadModel,
  validatePermanentDashboardNavigationRailShellReadModel,
} from "./permanentDashboardNavigationRailShellComponent.js";

export type PermanentDashboardNavigationRailShellIntegrationTarget =
  "permanent_dashboard_navigation_rail_shell_integration_boundary";

export type PermanentDashboardNavigationRailShellIntegrationSource =
  "permanent_dashboard_navigation_rail_shell_component";

export type PermanentDashboardNavigationRailShellIntegrationHost =
  "operator_dashboard_shell";

export type PermanentDashboardNavigationRailShellIntegrationSlot =
  "left_permanent_navigation_rail_slot";

export type PermanentDashboardNavigationRailShellIntegrationPlacement =
  "left_permanent_rail";

export type PermanentDashboardNavigationRailShellIntegrationContextualDrawerPolicy =
  "active_dashboard_only";

export type PermanentDashboardNavigationRailShellIntegrationTopCommunicationPolicy =
  "fullscreen_chat_separate";

export type PermanentDashboardNavigationRailShellIntegrationInput = {
  activeSurfaceId?: string;
  density?: PermanentDashboardNavigationRailVisualDensity;
};

export type PermanentDashboardNavigationRailShellIntegrationLayoutContract = {
  persistent: true;
  overlay: false;
  centerViewportOverlapAllowed: false;
  drawerSemanticsAllowedForMainDashboardList: false;
  contextualDrawerPolicy: PermanentDashboardNavigationRailShellIntegrationContextualDrawerPolicy;
  topCommunicationPolicy: PermanentDashboardNavigationRailShellIntegrationTopCommunicationPolicy;
  compactWidthPx: 104;
  expandedWidthPx: 284;
};

export type PermanentDashboardNavigationRailShellIntegrationBoundary = {
  target: PermanentDashboardNavigationRailShellIntegrationTarget;
  source: PermanentDashboardNavigationRailShellIntegrationSource;
  host: PermanentDashboardNavigationRailShellIntegrationHost;
  slot: PermanentDashboardNavigationRailShellIntegrationSlot;
  placement: PermanentDashboardNavigationRailShellIntegrationPlacement;
  componentExportName: "PermanentDashboardNavigationRail";
  shellReadModel: PermanentDashboardNavigationRailShellReadModel;
  layoutContract: PermanentDashboardNavigationRailShellIntegrationLayoutContract;
  appTsxHardcodingAllowed: false;
  directDashboardButtonHardcodingAllowed: false;
  directDrawerSemanticsAllowed: false;
};

export type PermanentDashboardNavigationRailShellIntegrationValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function buildPermanentDashboardNavigationRailShellIntegrationBoundary(
  input?: PermanentDashboardNavigationRailShellIntegrationInput,
): PermanentDashboardNavigationRailShellIntegrationBoundary {
  const shellReadModel = buildPermanentDashboardNavigationRailShellReadModel(input);

  return {
    target: "permanent_dashboard_navigation_rail_shell_integration_boundary",
    source: "permanent_dashboard_navigation_rail_shell_component",
    host: "operator_dashboard_shell",
    slot: "left_permanent_navigation_rail_slot",
    placement: "left_permanent_rail",
    componentExportName: "PermanentDashboardNavigationRail",
    shellReadModel,
    layoutContract: {
      persistent: true,
      overlay: false,
      centerViewportOverlapAllowed: false,
      drawerSemanticsAllowedForMainDashboardList: false,
      contextualDrawerPolicy: "active_dashboard_only",
      topCommunicationPolicy: "fullscreen_chat_separate",
      compactWidthPx: 104,
      expandedWidthPx: 284,
    },
    appTsxHardcodingAllowed: false,
    directDashboardButtonHardcodingAllowed: false,
    directDrawerSemanticsAllowed: false,
  };
}

export function validatePermanentDashboardNavigationRailShellIntegrationBoundary(
  boundary: PermanentDashboardNavigationRailShellIntegrationBoundary =
    buildPermanentDashboardNavigationRailShellIntegrationBoundary(),
): PermanentDashboardNavigationRailShellIntegrationValidation {
  const errors: string[] = [];

  if (boundary.target !== "permanent_dashboard_navigation_rail_shell_integration_boundary") {
    errors.push("target_must_be_permanent_dashboard_navigation_rail_shell_integration_boundary");
  }

  if (boundary.source !== "permanent_dashboard_navigation_rail_shell_component") {
    errors.push("source_must_be_permanent_dashboard_navigation_rail_shell_component");
  }

  if (boundary.host !== "operator_dashboard_shell") {
    errors.push("host_must_be_operator_dashboard_shell");
  }

  if (boundary.slot !== "left_permanent_navigation_rail_slot") {
    errors.push("slot_must_be_left_permanent_navigation_rail_slot");
  }

  if (boundary.placement !== "left_permanent_rail") {
    errors.push("placement_must_be_left_permanent_rail");
  }

  if (boundary.componentExportName !== "PermanentDashboardNavigationRail") {
    errors.push("component_export_must_be_permanent_dashboard_navigation_rail");
  }

  if (!boundary.layoutContract.persistent) {
    errors.push("layout_contract_must_be_persistent");
  }

  if (boundary.layoutContract.overlay) {
    errors.push("layout_contract_must_not_be_overlay");
  }

  if (boundary.layoutContract.centerViewportOverlapAllowed) {
    errors.push("layout_contract_must_not_overlap_center_viewport");
  }

  if (boundary.layoutContract.drawerSemanticsAllowedForMainDashboardList) {
    errors.push("main_dashboard_list_must_not_use_drawer_semantics");
  }

  if (boundary.layoutContract.contextualDrawerPolicy !== "active_dashboard_only") {
    errors.push("contextual_drawer_policy_must_be_active_dashboard_only");
  }

  if (boundary.layoutContract.topCommunicationPolicy !== "fullscreen_chat_separate") {
    errors.push("top_communication_policy_must_be_fullscreen_chat_separate");
  }

  if (boundary.layoutContract.compactWidthPx !== 104) {
    errors.push("compact_width_must_be_104");
  }

  if (boundary.layoutContract.expandedWidthPx !== 284) {
    errors.push("expanded_width_must_be_284");
  }

  if (boundary.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  if (boundary.directDashboardButtonHardcodingAllowed) {
    errors.push("direct_dashboard_button_hardcoding_forbidden");
  }

  if (boundary.directDrawerSemanticsAllowed) {
    errors.push("direct_drawer_semantics_forbidden");
  }

  const shellValidation =
    validatePermanentDashboardNavigationRailShellReadModel(
      boundary.shellReadModel,
    );

  if (!shellValidation.valid) {
    for (const error of shellValidation.errors) {
      errors.push(`shell_read_model_invalid:${error}`);
    }
  }

  if (boundary.shellReadModel.totalSections !== 19) {
    errors.push("shell_read_model_total_sections_must_be_19");
  }

  if (boundary.shellReadModel.totalItems !== 38) {
    errors.push("shell_read_model_total_items_must_be_38");
  }

  if (boundary.shellReadModel.selectedItems !== 1) {
    errors.push("shell_read_model_selected_items_must_be_1");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
