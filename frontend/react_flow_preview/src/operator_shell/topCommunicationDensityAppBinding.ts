import {
  buildTopCommunicationDensityReadModel,
  type TopCommunicationDensityInput,
} from "./topCommunicationDensityReadModel.js";
import type {
  TopCommunicationBlockId,
  TopCommunicationBlockState,
} from "./topCommunicationDensityPolicy.js";

export type TopCommunicationDensityAppBinding = {
  mode: ReturnType<typeof buildTopCommunicationDensityReadModel>["mode"];
  showSectionTabs: boolean;
  showSurfaceSelector: boolean;
  collapseSurfaceSelector: boolean;
  showSummaryChipLane: boolean;
  collapseSummaryChipLane: boolean;
  showSupportMeta: boolean;
  contentDominant: boolean;
  compactHeaderSpacing: boolean;
};

function resolveBlockState(
  input: TopCommunicationDensityInput,
  blockId: TopCommunicationBlockId,
): TopCommunicationBlockState {
  const readModel = buildTopCommunicationDensityReadModel(input);

  return (
    readModel.rows.find((row) => row.blockId === blockId)?.state ?? "hidden"
  );
}

export function buildTopCommunicationDensityAppBinding(
  input: TopCommunicationDensityInput,
): TopCommunicationDensityAppBinding {
  const readModel = buildTopCommunicationDensityReadModel(input);

  const sectionTabs = resolveBlockState(input, "section_tabs");
  const surfaceSelector = resolveBlockState(input, "surface_selector");
  const summaryChipLane = resolveBlockState(input, "summary_chip_lane");
  const supportMeta = resolveBlockState(input, "support_meta");
  const contentStream = resolveBlockState(input, "content_stream");

  return {
    mode: readModel.mode,
    showSectionTabs: sectionTabs !== "hidden",
    showSurfaceSelector: surfaceSelector !== "hidden",
    collapseSurfaceSelector: surfaceSelector === "collapsed",
    showSummaryChipLane: summaryChipLane !== "hidden",
    collapseSummaryChipLane: summaryChipLane === "collapsed",
    showSupportMeta: supportMeta !== "hidden",
    contentDominant: contentStream === "dominant",
    compactHeaderSpacing: readModel.mode === "normalized_density",
  };
}
