export type PanelNavigationPanelId =
  | "system_status"
  | "guard_chain"
  | "incidents"
  | "logs"
  | "topology"
  | "action_queue"
  | "approval_queue"
  | "audit_timeline";

export type PanelNavigationViewId =
  | "view_foundation_status"
  | "view_foundation_observability"
  | "view_operator_interaction";

export type PanelNavigationWorkspaceId =
  | "workspace_foundation_monitoring"
  | "workspace_operator_interaction";

export type PanelNavigationWorkspaceRole =
  | "foundation_monitoring"
  | "operator_interaction";

export type PanelNavigationBindingReason =
  | "foundation_visibility"
  | "operator_interaction_visibility";

export type PanelNavigationShellLanding =
  | "main_operator_secondary_foundation_reuse"
  | "main_operator_primary_operator_interaction";

export type PanelNavigationRegistryEntry = {
  panelId: PanelNavigationPanelId;
  order: number;
  title: string;
  navigationViewId: PanelNavigationViewId;
  workspaceId: PanelNavigationWorkspaceId;
  workspaceRole: PanelNavigationWorkspaceRole;
  bindingReason: PanelNavigationBindingReason;
  shellLanding: PanelNavigationShellLanding;
  visibleInNavigation: boolean;
  truthBound: boolean;
  operatorVisible: boolean;
  rationale: string;
};

export const panelNavigationRegistry:
  ReadonlyArray<PanelNavigationRegistryEntry> = [
    {
      panelId: "system_status",
      order: 1,
      title: "System Status",
      navigationViewId: "view_foundation_status",
      workspaceId: "workspace_foundation_monitoring",
      workspaceRole: "foundation_monitoring",
      bindingReason: "foundation_visibility",
      shellLanding: "main_operator_secondary_foundation_reuse",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Foundation status panel confirmed in audited foundation status view path.",
    },
    {
      panelId: "guard_chain",
      order: 2,
      title: "Guard Chain",
      navigationViewId: "view_foundation_status",
      workspaceId: "workspace_foundation_monitoring",
      workspaceRole: "foundation_monitoring",
      bindingReason: "foundation_visibility",
      shellLanding: "main_operator_secondary_foundation_reuse",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Guard-chain panel confirmed in audited foundation status view path.",
    },
    {
      panelId: "incidents",
      order: 3,
      title: "Incidents",
      navigationViewId: "view_foundation_status",
      workspaceId: "workspace_foundation_monitoring",
      workspaceRole: "foundation_monitoring",
      bindingReason: "foundation_visibility",
      shellLanding: "main_operator_secondary_foundation_reuse",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Incidents panel confirmed in audited foundation status view path.",
    },
    {
      panelId: "logs",
      order: 4,
      title: "Logs",
      navigationViewId: "view_foundation_observability",
      workspaceId: "workspace_foundation_monitoring",
      workspaceRole: "foundation_monitoring",
      bindingReason: "foundation_visibility",
      shellLanding: "main_operator_secondary_foundation_reuse",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Logs panel confirmed in audited foundation observability view path.",
    },
    {
      panelId: "topology",
      order: 5,
      title: "Topology",
      navigationViewId: "view_foundation_observability",
      workspaceId: "workspace_foundation_monitoring",
      workspaceRole: "foundation_monitoring",
      bindingReason: "foundation_visibility",
      shellLanding: "main_operator_secondary_foundation_reuse",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Topology panel confirmed in audited foundation observability view path.",
    },
    {
      panelId: "action_queue",
      order: 6,
      title: "Action Queue",
      navigationViewId: "view_operator_interaction",
      workspaceId: "workspace_operator_interaction",
      workspaceRole: "operator_interaction",
      bindingReason: "operator_interaction_visibility",
      shellLanding: "main_operator_primary_operator_interaction",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Action queue panel confirmed in audited operator interaction view path.",
    },
    {
      panelId: "approval_queue",
      order: 7,
      title: "Approval Queue",
      navigationViewId: "view_operator_interaction",
      workspaceId: "workspace_operator_interaction",
      workspaceRole: "operator_interaction",
      bindingReason: "operator_interaction_visibility",
      shellLanding: "main_operator_primary_operator_interaction",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Approval queue panel confirmed in audited operator interaction view path.",
    },
    {
      panelId: "audit_timeline",
      order: 8,
      title: "Audit Timeline",
      navigationViewId: "view_operator_interaction",
      workspaceId: "workspace_operator_interaction",
      workspaceRole: "operator_interaction",
      bindingReason: "operator_interaction_visibility",
      shellLanding: "main_operator_primary_operator_interaction",
      visibleInNavigation: true,
      truthBound: true,
      operatorVisible: true,
      rationale:
        "Audit timeline panel confirmed in audited operator interaction view path.",
    },
  ];

export function getPanelNavigationRegistryEntry(
  panelId: PanelNavigationPanelId,
): PanelNavigationRegistryEntry {
  const entry = panelNavigationRegistry.find(
    (candidate) => candidate.panelId === panelId,
  );

  if (!entry) {
    throw new Error(`Missing panel navigation entry for ${panelId}.`);
  }

  return entry;
}

export function getPanelNavigationOrder(): PanelNavigationPanelId[] {
  return panelNavigationRegistry.map((entry) => entry.panelId);
}

export function getPanelNavigationGroups(): ReadonlyArray<{
  navigationViewId: PanelNavigationViewId;
  title: string;
  panelIds: PanelNavigationPanelId[];
}> {
  const titles: Record<PanelNavigationViewId, string> = {
    view_foundation_status: "Foundation Status",
    view_foundation_observability: "Foundation Observability",
    view_operator_interaction: "Operator Interaction",
  };

  const order: readonly PanelNavigationViewId[] = [
    "view_foundation_status",
    "view_foundation_observability",
    "view_operator_interaction",
  ];

  return order.map((navigationViewId) => ({
    navigationViewId,
    title: titles[navigationViewId],
    panelIds: panelNavigationRegistry
      .filter(
        (entry) =>
          entry.navigationViewId === navigationViewId &&
          entry.visibleInNavigation,
      )
      .map((entry) => entry.panelId),
  }));
}
