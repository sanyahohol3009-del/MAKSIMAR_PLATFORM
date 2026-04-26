import { buildDefaultInspectPresentation } from "./graphInspectSemantics.js";
import {
  getPanelNavigationRegistryEntry,
  type PanelNavigationPanelId,
} from "./panelNavigationRegistry.js";

export type PanelNavigationInspectPresentation =
  ReturnType<typeof buildDefaultInspectPresentation>;

export function buildPanelNavigationInspectPresentation(
  panelId: PanelNavigationPanelId,
): PanelNavigationInspectPresentation {
  const entry = getPanelNavigationRegistryEntry(panelId);

  return {
    title: entry.title,
    subtitle:
      `Panel navigation lane for ${entry.navigationViewId} in ${entry.workspaceId}.`,
    semanticKind: "panel_navigation_binding",
    explanation: entry.rationale,
    sections: [
      {
        title: "Navigation Binding",
        items: [
          {
            key: "Panel Id",
            value: entry.panelId,
          },
          {
            key: "Navigation View",
            value: entry.navigationViewId,
          },
          {
            key: "Binding Reason",
            value: entry.bindingReason,
          },
        ],
      },
      {
        title: "Shell Placement",
        items: [
          {
            key: "Workspace Id",
            value: entry.workspaceId,
          },
          {
            key: "Workspace Role",
            value: entry.workspaceRole,
          },
          {
            key: "Shell Landing",
            value: entry.shellLanding,
          },
        ],
      },
    ],
  };
}
