import { buildOverlayDrawerLayoutContract } from "../overlayDrawerLayoutContract.js";

export type JarvisChatDrawerSectionId =
  | "conversation"
  | "project_context"
  | "command_handoff"
  | "diagnostics";

export type JarvisChatDrawerContract = {
  contractId: "jarvis_chat_drawer_contract_v1";
  drawerId: "top_chat_drawer";
  edge: "top";
  overlayOnly: true;
  collapsible: true;
  defaultState: "hidden";
  collapsedStripLabel: string;
  projectTitleStripVisibleWhenHidden: true;
  primarySurface: "jarvis_chat";
  sections: readonly JarvisChatDrawerSectionId[];
  preservesCenterCanvas: true;
  glassOverlay: true;
  undockable: true;
  handleLabel: string;
  overlayOpacity: number;
  backdropBlurPx: number;
  rationale: string;
};

export function buildJarvisChatDrawerContract():
  JarvisChatDrawerContract {
  const overlayContract = buildOverlayDrawerLayoutContract();

  return {
    contractId: "jarvis_chat_drawer_contract_v1",
    drawerId: "top_chat_drawer",
    edge: "top",
    overlayOnly: true,
    collapsible: true,
    defaultState: "hidden",
    collapsedStripLabel: "MAKSIMAR Unified Visual Shell Preview",
    projectTitleStripVisibleWhenHidden: true,
    primarySurface: "jarvis_chat",
    sections: [
      "conversation",
      "project_context",
      "command_handoff",
      "diagnostics",
    ],
    preservesCenterCanvas: true,
    glassOverlay: true,
    undockable: true,
    handleLabel: overlayContract.drawers.top.handleLabel,
    overlayOpacity: overlayContract.drawers.top.opacity,
    backdropBlurPx: overlayContract.drawers.top.backdropBlurPx,
    rationale:
      "The top communication drawer remains an overlay-only chat-first surface over an immutable fullscreen center canvas.",
  };
}
