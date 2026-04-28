export type AppShellPermanentRailLayoutOffsetsTarget =
  "appshell_permanent_rail_layout_offsets";

export type AppShellPermanentRailLayoutOffsetsReadModel = {
  target: AppShellPermanentRailLayoutOffsetsTarget;
  compactRailWidthPx: 104;
  expandedRailWidthPx: 284;
  visiblePermanentRailWidthPx: 284;
  centerViewportLeftOffsetPx: 284;
  activeDashboardLeftDrawerLeftOffsetPx: 284;
  leftDrawerHandleLeftOffsetPx: 284;
  summaryCardsLeftOffsetPx: 284;
  permanentRailIsDashboardSelector: true;
  activeLeftDrawerIsDashboardContext: true;
};

export type AppShellPermanentRailLayoutOffsetsValidation = {
  valid: boolean;
  errors: readonly string[];
};

export const PERMANENT_RAIL_COMPACT_WIDTH_PX = 104 as const;
export const PERMANENT_RAIL_EXPANDED_WIDTH_PX = 284 as const;

export const VISIBLE_PERMANENT_RAIL_WIDTH_PX =
  PERMANENT_RAIL_EXPANDED_WIDTH_PX;

export const CENTER_VIEWPORT_LEFT_OFFSET_PX =
  VISIBLE_PERMANENT_RAIL_WIDTH_PX;

export const ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX =
  VISIBLE_PERMANENT_RAIL_WIDTH_PX;

export const LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX =
  VISIBLE_PERMANENT_RAIL_WIDTH_PX;

export const SUMMARY_CARDS_LEFT_OFFSET_PX =
  VISIBLE_PERMANENT_RAIL_WIDTH_PX;

export function buildAppShellPermanentRailLayoutOffsetsReadModel(): AppShellPermanentRailLayoutOffsetsReadModel {
  return {
    target: "appshell_permanent_rail_layout_offsets",
    compactRailWidthPx: PERMANENT_RAIL_COMPACT_WIDTH_PX,
    expandedRailWidthPx: PERMANENT_RAIL_EXPANDED_WIDTH_PX,
    visiblePermanentRailWidthPx: VISIBLE_PERMANENT_RAIL_WIDTH_PX,
    centerViewportLeftOffsetPx: CENTER_VIEWPORT_LEFT_OFFSET_PX,
    activeDashboardLeftDrawerLeftOffsetPx:
      ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX,
    leftDrawerHandleLeftOffsetPx: LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX,
    summaryCardsLeftOffsetPx: SUMMARY_CARDS_LEFT_OFFSET_PX,
    permanentRailIsDashboardSelector: true,
    activeLeftDrawerIsDashboardContext: true,
  };
}

export function validateAppShellPermanentRailLayoutOffsetsReadModel(
  readModel: AppShellPermanentRailLayoutOffsetsReadModel =
    buildAppShellPermanentRailLayoutOffsetsReadModel(),
): AppShellPermanentRailLayoutOffsetsValidation {
  const errors: string[] = [];

  if (readModel.target !== "appshell_permanent_rail_layout_offsets") {
    errors.push("target_must_be_appshell_permanent_rail_layout_offsets");
  }

  if (readModel.compactRailWidthPx !== 104) {
    errors.push("compact_rail_width_must_be_104");
  }

  if (readModel.expandedRailWidthPx !== 284) {
    errors.push("expanded_rail_width_must_be_284");
  }

  if (readModel.visiblePermanentRailWidthPx !== 284) {
    errors.push("visible_permanent_rail_width_must_be_284");
  }

  if (
    readModel.centerViewportLeftOffsetPx !==
    readModel.visiblePermanentRailWidthPx
  ) {
    errors.push("center_viewport_offset_must_match_visible_rail_width");
  }

  if (
    readModel.activeDashboardLeftDrawerLeftOffsetPx !==
    readModel.visiblePermanentRailWidthPx
  ) {
    errors.push("active_left_drawer_offset_must_match_visible_rail_width");
  }

  if (
    readModel.leftDrawerHandleLeftOffsetPx !==
    readModel.visiblePermanentRailWidthPx
  ) {
    errors.push("left_handle_offset_must_match_visible_rail_width");
  }

  if (
    readModel.summaryCardsLeftOffsetPx !==
    readModel.visiblePermanentRailWidthPx
  ) {
    errors.push("summary_cards_offset_must_match_visible_rail_width");
  }

  if (!readModel.permanentRailIsDashboardSelector) {
    errors.push("permanent_rail_must_remain_dashboard_selector");
  }

  if (!readModel.activeLeftDrawerIsDashboardContext) {
    errors.push("active_left_drawer_must_remain_dashboard_context");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
