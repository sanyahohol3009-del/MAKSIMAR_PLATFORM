import {
  buildOperatorZoneVisibilityReadModel,
  type OperatorZoneVisibilityInput,
} from "./operatorZoneVisibilityReadModel.js";
import type { OperatorZoneVisibilityState } from "./operatorZoneVisibilityPolicy.js";

export type OperatorZoneAppBinding = {
  shellMode: ReturnType<typeof buildOperatorZoneVisibilityReadModel>["shellMode"];
  topVisibilityState: OperatorZoneVisibilityState;
  leftVisibilityState: OperatorZoneVisibilityState;
  rightVisibilityState: OperatorZoneVisibilityState;
  showTopCommunicationOverlay: boolean;
  showLeftDrawer: boolean;
  showRightDrawer: boolean;
  showLeftHandle: boolean;
  showRightHandle: boolean;
  showSummaryCards: boolean;
  showFooter: boolean;
  centerImmutableConfirmed: boolean;
};

function resolveZoneState(
  input: OperatorZoneVisibilityInput,
  zoneId:
    | "top_communication"
    | "left_navigation"
    | "right_context",
): OperatorZoneVisibilityState {
  const readModel = buildOperatorZoneVisibilityReadModel(input);
  return (
    readModel.rows.find((row) => row.zoneId === zoneId)?.visibilityState ??
    "hidden"
  );
}

export function buildOperatorZoneAppBinding(
  input: OperatorZoneVisibilityInput,
): OperatorZoneAppBinding {
  const readModel = buildOperatorZoneVisibilityReadModel(input);

  const topVisibilityState = resolveZoneState(input, "top_communication");
  const leftVisibilityState = resolveZoneState(input, "left_navigation");
  const rightVisibilityState = resolveZoneState(input, "right_context");

  return {
    shellMode: readModel.shellMode,
    topVisibilityState,
    leftVisibilityState,
    rightVisibilityState,
    showTopCommunicationOverlay:
      topVisibilityState === "fullscreen_overlay" ||
      topVisibilityState === "drawer_overlay",
    showLeftDrawer: leftVisibilityState === "drawer_overlay",
    showRightDrawer: rightVisibilityState === "drawer_overlay",
    showLeftHandle: readModel.shellMode !== "communication_focus",
    showRightHandle: readModel.shellMode !== "communication_focus",
    showSummaryCards: readModel.shellMode === "baseline",
    showFooter: true,
    centerImmutableConfirmed: readModel.centerImmutableConfirmed,
  };
}
