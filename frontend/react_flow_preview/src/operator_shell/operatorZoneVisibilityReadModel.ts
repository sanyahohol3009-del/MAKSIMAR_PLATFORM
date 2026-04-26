import {
  buildOperatorZoneVisibilityPolicy,
  type OperatorShellMode,
  type OperatorZonePolicyEntry,
  type OperatorZoneVisibilityState,
} from "./operatorZoneVisibilityPolicy.js";

export type OperatorZoneDrawerMode = "hidden" | "expanded";

export type OperatorZoneVisibilityInput = {
  topMode: OperatorZoneDrawerMode;
  leftMode: OperatorZoneDrawerMode;
  rightMode: OperatorZoneDrawerMode;
};

export type OperatorZoneVisibilityReadModel = {
  shellMode: OperatorShellMode;
  totalZones: number;
  hiddenZones: number;
  overlayZones: number;
  visibleZones: number;
  centerImmutableConfirmed: boolean;
  fullscreenCommunicationActive: boolean;
  rows: readonly OperatorZonePolicyEntry[];
};

function isOverlayState(
  visibilityState: OperatorZoneVisibilityState,
): boolean {
  return (
    visibilityState === "drawer_overlay" ||
    visibilityState === "fullscreen_overlay" ||
    visibilityState === "collapsed_strip"
  );
}

function isVisibleState(
  visibilityState: OperatorZoneVisibilityState,
): boolean {
  return visibilityState !== "hidden";
}

export function resolveOperatorShellMode(
  input: OperatorZoneVisibilityInput,
): OperatorShellMode {
  if (input.topMode === "expanded") {
    return "communication_focus";
  }

  if (input.leftMode === "expanded" && input.rightMode === "hidden") {
    return "left_navigation_focus";
  }

  if (input.rightMode === "expanded" && input.leftMode === "hidden") {
    return "right_context_focus";
  }

  return "baseline";
}

export function buildOperatorZoneVisibilityReadModel(
  input: OperatorZoneVisibilityInput,
): OperatorZoneVisibilityReadModel {
  const shellMode = resolveOperatorShellMode(input);
  const rows = buildOperatorZoneVisibilityPolicy(shellMode);

  const hiddenZones = rows.filter(
    (row) => row.visibilityState === "hidden",
  ).length;

  const overlayZones = rows.filter((row) =>
    isOverlayState(row.visibilityState),
  ).length;

  const visibleZones = rows.filter((row) =>
    isVisibleState(row.visibilityState),
  ).length;

  return {
    shellMode,
    totalZones: rows.length,
    hiddenZones,
    overlayZones,
    visibleZones,
    centerImmutableConfirmed: rows.every((row) => row.centerImmutable),
    fullscreenCommunicationActive:
      shellMode === "communication_focus",
    rows,
  };
}
