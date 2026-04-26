import {
  getPanelNavigationGroups,
  getPanelNavigationRegistryEntry,
  panelNavigationRegistry,
  type PanelNavigationPanelId,
} from "./panelNavigationRegistry.js";

export type PanelNavigationReadRow = {
  panelId: PanelNavigationPanelId;
  title: string;
  navigationViewId: string;
  workspaceId: string;
  workspaceRole: string;
  bindingReason: string;
  shellLanding: string;
  truthBound: boolean;
  operatorVisible: boolean;
};

export type PanelNavigationReadModel = {
  totalPanels: number;
  foundationPanels: number;
  interactionPanels: number;
  groupedNavigation: ReadonlyArray<{
    navigationViewId: string;
    title: string;
    rows: PanelNavigationReadRow[];
  }>;
};

export function buildPanelNavigationReadModel(): PanelNavigationReadModel {
  const groupedNavigation = getPanelNavigationGroups().map((group) => ({
    navigationViewId: group.navigationViewId,
    title: group.title,
    rows: group.panelIds.map((panelId) => {
      const entry = getPanelNavigationRegistryEntry(panelId);
      return {
        panelId: entry.panelId,
        title: entry.title,
        navigationViewId: entry.navigationViewId,
        workspaceId: entry.workspaceId,
        workspaceRole: entry.workspaceRole,
        bindingReason: entry.bindingReason,
        shellLanding: entry.shellLanding,
        truthBound: entry.truthBound,
        operatorVisible: entry.operatorVisible,
      };
    }),
  }));

  return {
    totalPanels: panelNavigationRegistry.length,
    foundationPanels: panelNavigationRegistry.filter(
      (entry) => entry.workspaceRole === "foundation_monitoring",
    ).length,
    interactionPanels: panelNavigationRegistry.filter(
      (entry) => entry.workspaceRole === "operator_interaction",
    ).length,
    groupedNavigation,
  };
}
