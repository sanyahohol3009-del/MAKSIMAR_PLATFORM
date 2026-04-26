import {
  buildOverlayDrawerLayoutContract,
  type LeftDrawerSection,
  type OverlayDrawerDockMode,
  type OverlayDrawerId,
  type OverlayDrawerMode,
  type RightDrawerSection,
  type TopDrawerSection,
} from "./overlayDrawerLayoutContract.js";

type DrawerSection =
  | LeftDrawerSection
  | RightDrawerSection
  | TopDrawerSection;

type DrawerSectionRow = {
  sectionId: DrawerSection;
  title: string;
};

type DrawerSummary = {
  drawerId: OverlayDrawerId;
  defaultMode: OverlayDrawerMode;
  dockMode: OverlayDrawerDockMode;
  handleLabel: string;
  visualStyle: string;
  opacity: number;
  backdropBlurPx: number;
  expandedSizePx: number;
  sections: readonly DrawerSectionRow[];
};

export type OverlayDrawerLayoutReadModel = {
  totalDrawers: number;
  hiddenByDefaultCount: number;
  undockCapableCount: number;
  overlayOnly: boolean;
  centerCanvasPolicy: string;
  centerCanvasAlwaysVisible: boolean;
  centerCanvasMovesOnDrawerOpen: boolean;
  centerCanvasResizesOnDrawerOpen: boolean;
  topDrawerDefaultsToChat: boolean;
  drawerSummaries: readonly DrawerSummary[];
};

function getSectionTitle(sectionId: DrawerSection): string {
  switch (sectionId) {
    case "visual_registry_navigation":
      return "Visual Registry Navigation";
    case "panel_navigation":
      return "Panel Navigation";
    case "embedded_chat_context":
      return "Embedded Chat Context";
    case "inspect":
      return "Inspect";
    case "memory_knowledge":
      return "Memory / Knowledge";
    case "panel_family_taxonomy_exposure":
      return "Panel Family / Taxonomy / Exposure";
    case "jarvis_chat":
      return "JARVIS Chat";
    case "chat_history":
      return "Chat History";
    case "chat_code_output":
      return "Chat Code Output";
    case "chat_context_summary":
      return "Chat Context Summary";
  }
}

export function buildOverlayDrawerLayoutReadModel():
  OverlayDrawerLayoutReadModel {
  const contract = buildOverlayDrawerLayoutContract();
  const drawers = [
    contract.drawers.left,
    contract.drawers.right,
    contract.drawers.top,
  ] as const;

  return {
    totalDrawers: drawers.length,
    hiddenByDefaultCount: drawers.filter(
      (drawer) => drawer.defaultMode === "hidden",
    ).length,
    undockCapableCount: drawers.filter(
      (drawer) => drawer.allowsUndock,
    ).length,
    overlayOnly: drawers.every(
      (drawer) =>
        drawer.pushesCenterCanvas === false &&
        drawer.resizesCenterCanvas === false &&
        drawer.blocksCenterCanvasLayout === false,
    ),
    centerCanvasPolicy: contract.centerCanvasPolicy,
    centerCanvasAlwaysVisible: contract.centerCanvasAlwaysVisible,
    centerCanvasMovesOnDrawerOpen: contract.centerCanvasMovesOnDrawerOpen,
    centerCanvasResizesOnDrawerOpen: contract.centerCanvasResizesOnDrawerOpen,
    topDrawerDefaultsToChat:
      contract.drawers.top.activeSection === "jarvis_chat",
    drawerSummaries: drawers.map((drawer) => ({
      drawerId: drawer.drawerId,
      defaultMode: drawer.defaultMode,
      dockMode: drawer.dockMode,
      handleLabel: drawer.handleLabel,
      visualStyle: drawer.visualStyle,
      opacity: drawer.opacity,
      backdropBlurPx: drawer.backdropBlurPx,
      expandedSizePx: drawer.expandedSizePx,
      sections: drawer.availableSections.map((sectionId) => ({
        sectionId,
        title: getSectionTitle(sectionId),
      })),
    })),
  };
}
