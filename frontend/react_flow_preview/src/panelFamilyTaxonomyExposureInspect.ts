import { buildDefaultInspectPresentation } from "./graphInspectSemantics.js";
import {
  getPanelFamilyTaxonomyExposureEntry,
  type PanelTaxonomyPanelId,
} from "./panelFamilyTaxonomyExposureRegistry.js";

export type PanelFamilyTaxonomyExposureInspectPresentation =
  ReturnType<typeof buildDefaultInspectPresentation>;

export function buildPanelFamilyTaxonomyExposureInspectPresentation(
  panelId: PanelTaxonomyPanelId,
): PanelFamilyTaxonomyExposureInspectPresentation {
  const entry = getPanelFamilyTaxonomyExposureEntry(panelId);

  return {
    title: entry.title,
    subtitle:
      `Family/taxonomy/exposure lane for ${entry.shellTaxonomy}.`,
    semanticKind: "panel_family_taxonomy_exposure",
    explanation: entry.rationale,
    sections: [
      {
        title: "Family and Taxonomy",
        items: [
          {
            key: "Panel Id",
            value: entry.panelId,
          },
          {
            key: "Panel Family",
            value: entry.panelFamily,
          },
          {
            key: "Panel Kind",
            value: entry.panelKind,
          },
          {
            key: "Shell Taxonomy",
            value: entry.shellTaxonomy,
          },
        ],
      },
      {
        title: "Exposure Semantics",
        items: [
          {
            key: "Exposure Level",
            value: entry.exposureLevel,
          },
          {
            key: "Visibility Policy",
            value: entry.visibilityPolicy,
          },
          {
            key: "Visible In Main Dashboard",
            value: String(entry.visibleInMainDashboard),
          },
          {
            key: "Visible In Navigation",
            value: String(entry.visibleInNavigation),
          },
        ],
      },
    ],
  };
}
