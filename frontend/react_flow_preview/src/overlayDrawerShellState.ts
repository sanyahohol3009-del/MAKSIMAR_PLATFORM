import {
  buildOverlayDrawerLayoutContract,
  type LeftDrawerSection,
  type OverlayDrawerMode,
  type RightDrawerSection,
  type TopDrawerSection,
} from "./overlayDrawerLayoutContract.js";

export type OverlayDrawerShellState = {
  leftMode: OverlayDrawerMode;
  rightMode: OverlayDrawerMode;
  topMode: OverlayDrawerMode;
  activeLeftSection: LeftDrawerSection;
  activeRightSection: RightDrawerSection;
  activeTopSection: TopDrawerSection;
};

export function buildInitialOverlayDrawerShellState():
  OverlayDrawerShellState {
  const contract = buildOverlayDrawerLayoutContract();

  return {
    leftMode: contract.drawers.left.defaultMode,
    rightMode: contract.drawers.right.defaultMode,
    topMode: contract.drawers.top.defaultMode,
    activeLeftSection: contract.drawers.left.activeSection,
    activeRightSection: contract.drawers.right.activeSection,
    activeTopSection: contract.drawers.top.activeSection,
  };
}

export function toggleOverlayDrawerMode(
  currentMode: OverlayDrawerMode,
): OverlayDrawerMode {
  return currentMode === "hidden" ? "expanded" : "hidden";
}
