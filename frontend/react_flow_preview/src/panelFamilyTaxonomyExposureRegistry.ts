export type PanelTaxonomyPanelId =
  | "system_status"
  | "guard_chain"
  | "incidents"
  | "logs"
  | "topology"
  | "action_queue"
  | "approval_queue"
  | "audit_timeline";

export type PanelMetadataFamily =
  | "foundation"
  | "interaction";

export type PanelShellTaxonomy =
  | "foundation_status"
  | "foundation_observability"
  | "operator_interaction";

export type PanelExposureLevel =
  | "operator_visible";

export type PanelVisibilityPolicy =
  | "always_visible"
  | "policy_visible";

export type PanelFamilyTaxonomyExposureEntry = {
  panelId: PanelTaxonomyPanelId;
  order: number;
  title: string;
  panelFamily: PanelMetadataFamily;
  panelKind: string;
  shellTaxonomy: PanelShellTaxonomy;
  exposureLevel: PanelExposureLevel;
  visibilityPolicy: PanelVisibilityPolicy;
  visibleInMainDashboard: boolean;
  visibleInNavigation: boolean;
  operatorVisible: boolean;
  rationale: string;
};

export const panelFamilyTaxonomyExposureRegistry:
  ReadonlyArray<PanelFamilyTaxonomyExposureEntry> = [
    {
      panelId: "system_status",
      order: 1,
      title: "System Status",
      panelFamily: "foundation",
      panelKind: "status",
      shellTaxonomy: "foundation_status",
      exposureLevel: "operator_visible",
      visibilityPolicy: "always_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Foundation status panel with always-visible operator exposure.",
    },
    {
      panelId: "guard_chain",
      order: 2,
      title: "Guard Chain",
      panelFamily: "foundation",
      panelKind: "guard",
      shellTaxonomy: "foundation_status",
      exposureLevel: "operator_visible",
      visibilityPolicy: "always_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Foundation status panel with always-visible operator exposure.",
    },
    {
      panelId: "incidents",
      order: 3,
      title: "Incidents",
      panelFamily: "foundation",
      panelKind: "incident",
      shellTaxonomy: "foundation_status",
      exposureLevel: "operator_visible",
      visibilityPolicy: "always_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Foundation status panel with always-visible operator exposure.",
    },
    {
      panelId: "logs",
      order: 4,
      title: "Logs",
      panelFamily: "foundation",
      panelKind: "log",
      shellTaxonomy: "foundation_observability",
      exposureLevel: "operator_visible",
      visibilityPolicy: "always_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Foundation observability panel with always-visible operator exposure.",
    },
    {
      panelId: "topology",
      order: 5,
      title: "Topology",
      panelFamily: "foundation",
      panelKind: "topology",
      shellTaxonomy: "foundation_observability",
      exposureLevel: "operator_visible",
      visibilityPolicy: "always_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Foundation observability panel with always-visible operator exposure.",
    },
    {
      panelId: "action_queue",
      order: 6,
      title: "Action Queue",
      panelFamily: "interaction",
      panelKind: "queue",
      shellTaxonomy: "operator_interaction",
      exposureLevel: "operator_visible",
      visibilityPolicy: "policy_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Operator interaction panel exposed through policy-visible interaction path.",
    },
    {
      panelId: "approval_queue",
      order: 7,
      title: "Approval Queue",
      panelFamily: "interaction",
      panelKind: "queue",
      shellTaxonomy: "operator_interaction",
      exposureLevel: "operator_visible",
      visibilityPolicy: "policy_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Operator interaction panel exposed through policy-visible interaction path.",
    },
    {
      panelId: "audit_timeline",
      order: 8,
      title: "Audit Timeline",
      panelFamily: "interaction",
      panelKind: "audit",
      shellTaxonomy: "operator_interaction",
      exposureLevel: "operator_visible",
      visibilityPolicy: "policy_visible",
      visibleInMainDashboard: true,
      visibleInNavigation: true,
      operatorVisible: true,
      rationale:
        "Operator interaction panel exposed through policy-visible interaction path.",
    },
  ];

export function getPanelFamilyTaxonomyExposureEntry(
  panelId: PanelTaxonomyPanelId,
): PanelFamilyTaxonomyExposureEntry {
  const entry = panelFamilyTaxonomyExposureRegistry.find(
    (candidate) => candidate.panelId === panelId,
  );

  if (!entry) {
    throw new Error(`Missing family/taxonomy/exposure entry for ${panelId}.`);
  }

  return entry;
}

export function getPanelFamilyTaxonomyGroups(): ReadonlyArray<{
  shellTaxonomy: PanelShellTaxonomy;
  title: string;
  panelIds: PanelTaxonomyPanelId[];
}> {
  const titles: Record<PanelShellTaxonomy, string> = {
    foundation_status: "Foundation Status",
    foundation_observability: "Foundation Observability",
    operator_interaction: "Operator Interaction",
  };

  const order: readonly PanelShellTaxonomy[] = [
    "foundation_status",
    "foundation_observability",
    "operator_interaction",
  ];

  return order.map((shellTaxonomy) => ({
    shellTaxonomy,
    title: titles[shellTaxonomy],
    panelIds: panelFamilyTaxonomyExposureRegistry
      .filter(
        (entry) =>
          entry.shellTaxonomy === shellTaxonomy &&
          entry.visibleInNavigation,
      )
      .map((entry) => entry.panelId),
  }));
}
