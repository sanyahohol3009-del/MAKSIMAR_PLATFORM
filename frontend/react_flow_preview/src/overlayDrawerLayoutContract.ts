export type OverlayDrawerId =
  | "left"
  | "right"
  | "top";

export type OverlayDrawerMode =
  | "hidden"
  | "peek"
  | "expanded";

export type OverlayDrawerDockMode =
  | "overlay"
  | "undocked_secondary_display";

export type OverlayDrawerVisualStyle =
  | "glass_overlay";

export type CenterCanvasPolicy =
  | "persistent_fullscreen_canvas";

export type LeftDrawerSection =
  | "visual_registry_navigation"
  | "panel_navigation"
  | "embedded_chat_context";

export type RightDrawerSection =
  | "inspect"
  | "memory_knowledge"
  | "panel_navigation"
  | "panel_family_taxonomy_exposure"
  | "embedded_chat_context";

export type TopDrawerSection =
  | "jarvis_chat"
  | "chat_history"
  | "chat_code_output"
  | "chat_context_summary";

export type OverlayDrawerContractState<TSection extends string> = {
  drawerId: OverlayDrawerId;
  defaultMode: OverlayDrawerMode;
  activeSection: TSection;
  availableSections: readonly TSection[];
  visualStyle: OverlayDrawerVisualStyle;
  dockMode: OverlayDrawerDockMode;
  handleLabel: string;
  peekSizePx: number;
  expandedSizePx: number;
  opacity: number;
  backdropBlurPx: number;
  closesOnHandleClick: boolean;
  opensOnHandleClick: boolean;
  pushesCenterCanvas: boolean;
  resizesCenterCanvas: boolean;
  blocksCenterCanvasLayout: boolean;
  allowsUndock: boolean;
};

export type OverlayDrawerLayoutContract = {
  contractId: "overlay_drawer_layout_contract";
  schemaVersion: "v1";
  centerCanvasPolicy: CenterCanvasPolicy;
  centerCanvasAlwaysVisible: boolean;
  centerCanvasMovesOnDrawerOpen: false;
  centerCanvasResizesOnDrawerOpen: false;
  centerCanvasIsPrimaryVisualSurface: true;
  drawers: {
    left: OverlayDrawerContractState<LeftDrawerSection>;
    right: OverlayDrawerContractState<RightDrawerSection>;
    top: OverlayDrawerContractState<TopDrawerSection>;
  };
  rationale: string;
};

export function buildOverlayDrawerLayoutContract():
  OverlayDrawerLayoutContract {
  return {
    contractId: "overlay_drawer_layout_contract",
    schemaVersion: "v1",
    centerCanvasPolicy: "persistent_fullscreen_canvas",
    centerCanvasAlwaysVisible: true,
    centerCanvasMovesOnDrawerOpen: false,
    centerCanvasResizesOnDrawerOpen: false,
    centerCanvasIsPrimaryVisualSurface: true,
    drawers: {
      left: {
        drawerId: "left",
        defaultMode: "hidden",
        activeSection: "visual_registry_navigation",
        availableSections: [
          "visual_registry_navigation",
          "panel_navigation",
          "embedded_chat_context",
        ],
        visualStyle: "glass_overlay",
        dockMode: "overlay",
        handleLabel: "◂ NAV",
        peekSizePx: 68,
        expandedSizePx: 360,
        opacity: 0.78,
        backdropBlurPx: 18,
        closesOnHandleClick: true,
        opensOnHandleClick: true,
        pushesCenterCanvas: false,
        resizesCenterCanvas: false,
        blocksCenterCanvasLayout: false,
        allowsUndock: true,
      },
      right: {
        drawerId: "right",
        defaultMode: "hidden",
        activeSection: "inspect",
        availableSections: [
          "inspect",
          "memory_knowledge",
          "panel_navigation",
          "panel_family_taxonomy_exposure",
          "embedded_chat_context",
        ],
        visualStyle: "glass_overlay",
        dockMode: "overlay",
        handleLabel: "CTX ▸",
        peekSizePx: 68,
        expandedSizePx: 420,
        opacity: 0.78,
        backdropBlurPx: 18,
        closesOnHandleClick: true,
        opensOnHandleClick: true,
        pushesCenterCanvas: false,
        resizesCenterCanvas: false,
        blocksCenterCanvasLayout: false,
        allowsUndock: true,
      },
      top: {
        drawerId: "top",
        defaultMode: "hidden",
        activeSection: "jarvis_chat",
        availableSections: [
          "jarvis_chat",
          "chat_history",
          "chat_code_output",
          "chat_context_summary",
        ],
        visualStyle: "glass_overlay",
        dockMode: "overlay",
        handleLabel: "CHAT ▾",
        peekSizePx: 56,
        expandedSizePx: 320,
        opacity: 0.72,
        backdropBlurPx: 20,
        closesOnHandleClick: true,
        opensOnHandleClick: true,
        pushesCenterCanvas: false,
        resizesCenterCanvas: false,
        blocksCenterCanvasLayout: false,
        allowsUndock: true,
      },
    },
    rationale:
      "Operator shell drawers must behave as transparent overlays over a persistent fullscreen center canvas, without moving or resizing the main visual surface.",
  };
}
