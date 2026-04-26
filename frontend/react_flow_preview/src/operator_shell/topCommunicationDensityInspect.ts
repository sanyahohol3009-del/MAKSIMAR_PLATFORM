import {
  buildTopCommunicationDensityReadModel,
  type TopCommunicationDensityInput,
} from "./topCommunicationDensityReadModel.js";

export type TopCommunicationDensityInspectPresentation = {
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

export function buildTopCommunicationDensityInspectPresentation(
  input: TopCommunicationDensityInput,
): TopCommunicationDensityInspectPresentation {
  const readModel = buildTopCommunicationDensityReadModel(input);

  return {
    title: "Top Communication Density",
    subtitle: readModel.mode,
    semanticKind: "top_communication_density",
    explanation:
      "This presentation describes how communication-layer blocks are reduced or emphasized so the fullscreen communication surface stays readable.",
    sections: [
      {
        title: "Density Mode",
        items: [
          { key: "Mode", value: readModel.mode },
          {
            key: "Content Dominant",
            value: String(readModel.contentDominant),
          },
        ],
      },
      {
        title: "Density Summary",
        items: [
          { key: "Total Blocks", value: String(readModel.totalBlocks) },
          { key: "Hidden Blocks", value: String(readModel.hiddenBlocks) },
          { key: "Collapsed Blocks", value: String(readModel.collapsedBlocks) },
          { key: "Dominant Blocks", value: String(readModel.dominantBlocks) },
        ],
      },
      {
        title: "Block States",
        items: readModel.rows.map((row) => ({
          key: row.title,
          value: row.state,
        })),
      },
    ],
  };
}
