import {
  getPanelFamilyTaxonomyExposureEntry,
  getPanelFamilyTaxonomyGroups,
  panelFamilyTaxonomyExposureRegistry,
  type PanelTaxonomyPanelId,
} from "./panelFamilyTaxonomyExposureRegistry.js";

export type PanelFamilyTaxonomyExposureReadModel = {
  totalPanels: number;
  foundationPanels: number;
  interactionPanels: number;
  alwaysVisiblePanels: number;
  policyVisiblePanels: number;
  groupedTaxonomy: ReadonlyArray<{
    shellTaxonomy: string;
    title: string;
    rows: ReadonlyArray<{
      panelId: PanelTaxonomyPanelId;
      title: string;
      panelFamily: string;
      panelKind: string;
      exposureLevel: string;
      visibilityPolicy: string;
    }>;
  }>;
};

export function buildPanelFamilyTaxonomyExposureReadModel():
  PanelFamilyTaxonomyExposureReadModel {
  const groupedTaxonomy = getPanelFamilyTaxonomyGroups().map((group) => ({
    shellTaxonomy: group.shellTaxonomy,
    title: group.title,
    rows: group.panelIds.map((panelId) => {
      const entry = getPanelFamilyTaxonomyExposureEntry(panelId);
      return {
        panelId: entry.panelId,
        title: entry.title,
        panelFamily: entry.panelFamily,
        panelKind: entry.panelKind,
        exposureLevel: entry.exposureLevel,
        visibilityPolicy: entry.visibilityPolicy,
      };
    }),
  }));

  return {
    totalPanels: panelFamilyTaxonomyExposureRegistry.length,
    foundationPanels: panelFamilyTaxonomyExposureRegistry.filter(
      (entry) => entry.panelFamily === "foundation",
    ).length,
    interactionPanels: panelFamilyTaxonomyExposureRegistry.filter(
      (entry) => entry.panelFamily === "interaction",
    ).length,
    alwaysVisiblePanels: panelFamilyTaxonomyExposureRegistry.filter(
      (entry) => entry.visibilityPolicy === "always_visible",
    ).length,
    policyVisiblePanels: panelFamilyTaxonomyExposureRegistry.filter(
      (entry) => entry.visibilityPolicy === "policy_visible",
    ).length,
    groupedTaxonomy,
  };
}
