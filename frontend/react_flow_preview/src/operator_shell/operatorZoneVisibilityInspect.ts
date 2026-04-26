import {
  buildOperatorZoneVisibilityReadModel,
  type OperatorZoneVisibilityInput,
} from "./operatorZoneVisibilityReadModel.js";

export type OperatorZoneVisibilityInspectPresentation = {
  title: string;
  subtitle: string;
  semanticKind: string;
  explanation: string;
  sections: readonly {
    title: string;
    items: readonly {
      key: string;
      value: string;
    }[];
  }[];
};

export function buildOperatorZoneVisibilityInspectPresentation(
  input: OperatorZoneVisibilityInput,
): OperatorZoneVisibilityInspectPresentation {
  const readModel = buildOperatorZoneVisibilityReadModel(input);

  return {
    title: "Operator Zone Visibility",
    subtitle: readModel.shellMode,
    semanticKind: "operator_zone_visibility",
    explanation:
      "This presentation describes which shell zones are visible, suppressed, or overlayed for the current operator-shell mode.",
    sections: [
      {
        title: "Shell Mode",
        items: [
          { key: "Mode", value: readModel.shellMode },
          {
            key: "Fullscreen Communication",
            value: String(readModel.fullscreenCommunicationActive),
          },
          {
            key: "Center Immutable",
            value: String(readModel.centerImmutableConfirmed),
          },
        ],
      },
      {
        title: "Visibility Summary",
        items: [
          { key: "Total Zones", value: String(readModel.totalZones) },
          { key: "Visible Zones", value: String(readModel.visibleZones) },
          { key: "Hidden Zones", value: String(readModel.hiddenZones) },
          { key: "Overlay Zones", value: String(readModel.overlayZones) },
        ],
      },
      {
        title: "Zone States",
        items: readModel.rows.map((row) => ({
          key: row.title,
          value: row.visibilityState,
        })),
      },
    ],
  };
}
