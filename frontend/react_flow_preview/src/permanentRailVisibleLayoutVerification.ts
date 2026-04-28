import type {
  AppShellPermanentRailVisibleWiringContract,
} from "./appShellPermanentRailVisibleWiringContract.js";
import {
  buildAppShellPermanentRailVisibleWiringContract,
  validateAppShellPermanentRailVisibleWiringContract,
} from "./appShellPermanentRailVisibleWiringContract.js";

export type PermanentRailVisibleLayoutVerificationTarget =
  "permanent_rail_visible_layout_verification";

export type PermanentRailVisibleLayoutVerificationSource =
  "appshell_permanent_rail_visible_wiring_contract";

export type PermanentRailVisibleLayoutVerificationStatus =
  "layout_verified";

export type PermanentRailVisibleLayoutVerificationReadModel = {
  target: PermanentRailVisibleLayoutVerificationTarget;
  source: PermanentRailVisibleLayoutVerificationSource;
  status: PermanentRailVisibleLayoutVerificationStatus;
  contract: AppShellPermanentRailVisibleWiringContract;
  railBeforeCenterViewport: boolean;
  railPersistent: true;
  railOverlay: false;
  railDrawer: false;
  railMayOverlapCenterViewport: false;
  centerViewportUsesRemainingWidth: boolean;
  contextualDrawersActiveDashboardOnly: boolean;
  contextualDrawersMayContainMainDashboardList: false;
  topChatSeparate: boolean;
  topChatMayContainDashboardNavigation: false;
  appTsxMayOnlyWireShellSlot: true;
  manualDashboardButtonListAllowed: false;
  manualRendererRouteLogicAllowed: false;
  manualTaxonomyDuplicationAllowed: false;
};

export type PermanentRailVisibleLayoutVerificationValidation = {
  valid: boolean;
  errors: readonly string[];
};

export function buildPermanentRailVisibleLayoutVerification(
  contract: AppShellPermanentRailVisibleWiringContract =
    buildAppShellPermanentRailVisibleWiringContract(),
): PermanentRailVisibleLayoutVerificationReadModel {
  return {
    target: "permanent_rail_visible_layout_verification",
    source: "appshell_permanent_rail_visible_wiring_contract",
    status: "layout_verified",
    contract,
    railBeforeCenterViewport:
      contract.railSlot.placement === "before_center_viewport",
    railPersistent: contract.railSlot.persistent,
    railOverlay: contract.railSlot.overlay,
    railDrawer: contract.railSlot.drawer,
    railMayOverlapCenterViewport: contract.railSlot.mayOverlapCenterViewport,
    centerViewportUsesRemainingWidth:
      contract.centerViewportSlot.widthPolicy === "remaining_shell_width",
    contextualDrawersActiveDashboardOnly:
      contract.contextualDrawers.policy === "active_dashboard_only",
    contextualDrawersMayContainMainDashboardList:
      contract.contextualDrawers.mayContainMainDashboardList,
    topChatSeparate:
      contract.topCommunication.policy === "fullscreen_chat_separate",
    topChatMayContainDashboardNavigation:
      contract.topCommunication.mayContainDashboardNavigation,
    appTsxMayOnlyWireShellSlot: true,
    manualDashboardButtonListAllowed: contract.appTsxDirectButtonListAllowed,
    manualRendererRouteLogicAllowed:
      contract.appTsxDirectRendererRouteLogicAllowed,
    manualTaxonomyDuplicationAllowed:
      contract.appTsxDirectTaxonomyDuplicationAllowed,
  };
}

export function validatePermanentRailVisibleLayoutVerification(
  readModel: PermanentRailVisibleLayoutVerificationReadModel =
    buildPermanentRailVisibleLayoutVerification(),
): PermanentRailVisibleLayoutVerificationValidation {
  const errors: string[] = [];

  if (readModel.target !== "permanent_rail_visible_layout_verification") {
    errors.push("target_must_be_permanent_rail_visible_layout_verification");
  }

  if (readModel.source !== "appshell_permanent_rail_visible_wiring_contract") {
    errors.push("source_must_be_appshell_permanent_rail_visible_wiring_contract");
  }

  if (readModel.status !== "layout_verified") {
    errors.push("status_must_be_layout_verified");
  }

  const contractValidation =
    validateAppShellPermanentRailVisibleWiringContract(readModel.contract);

  if (!contractValidation.valid) {
    for (const error of contractValidation.errors) {
      errors.push(`visible_wiring_contract_invalid:${error}`);
    }
  }

  if (!readModel.railBeforeCenterViewport) {
    errors.push("rail_must_be_before_center_viewport");
  }

  if (!readModel.railPersistent) {
    errors.push("rail_must_be_persistent");
  }

  if (readModel.railOverlay) {
    errors.push("rail_must_not_be_overlay");
  }

  if (readModel.railDrawer) {
    errors.push("rail_must_not_be_drawer");
  }

  if (readModel.railMayOverlapCenterViewport) {
    errors.push("rail_must_not_overlap_center_viewport");
  }

  if (!readModel.centerViewportUsesRemainingWidth) {
    errors.push("center_viewport_must_use_remaining_width");
  }

  if (!readModel.contextualDrawersActiveDashboardOnly) {
    errors.push("contextual_drawers_must_be_active_dashboard_only");
  }

  if (readModel.contextualDrawersMayContainMainDashboardList) {
    errors.push("contextual_drawers_must_not_contain_main_dashboard_list");
  }

  if (!readModel.topChatSeparate) {
    errors.push("top_chat_must_remain_separate");
  }

  if (readModel.topChatMayContainDashboardNavigation) {
    errors.push("top_chat_must_not_contain_dashboard_navigation");
  }

  if (!readModel.appTsxMayOnlyWireShellSlot) {
    errors.push("app_tsx_may_only_wire_shell_slot");
  }

  if (readModel.manualDashboardButtonListAllowed) {
    errors.push("manual_dashboard_button_list_forbidden");
  }

  if (readModel.manualRendererRouteLogicAllowed) {
    errors.push("manual_renderer_route_logic_forbidden");
  }

  if (readModel.manualTaxonomyDuplicationAllowed) {
    errors.push("manual_taxonomy_duplication_forbidden");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
