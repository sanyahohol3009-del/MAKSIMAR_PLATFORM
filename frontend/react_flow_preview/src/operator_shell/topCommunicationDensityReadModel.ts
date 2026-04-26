import {
  buildTopCommunicationDensityPolicy,
  type TopCommunicationBlockState,
  type TopCommunicationDensityMode,
  type TopCommunicationDensityPolicyEntry,
} from "./topCommunicationDensityPolicy.js";

export type TopCommunicationDensityInput = {
  fullscreenCommunication: boolean;
};

export type TopCommunicationDensityReadModel = {
  mode: TopCommunicationDensityMode;
  totalBlocks: number;
  hiddenBlocks: number;
  collapsedBlocks: number;
  dominantBlocks: number;
  contentDominant: boolean;
  rows: readonly TopCommunicationDensityPolicyEntry[];
};

function isHidden(state: TopCommunicationBlockState): boolean {
  return state === "hidden";
}

function isCollapsed(state: TopCommunicationBlockState): boolean {
  return state === "collapsed";
}

function isDominant(state: TopCommunicationBlockState): boolean {
  return state === "dominant";
}

export function resolveTopCommunicationDensityMode(
  input: TopCommunicationDensityInput,
): TopCommunicationDensityMode {
  return input.fullscreenCommunication
    ? "normalized_density"
    : "baseline_density";
}

export function buildTopCommunicationDensityReadModel(
  input: TopCommunicationDensityInput,
): TopCommunicationDensityReadModel {
  const mode = resolveTopCommunicationDensityMode(input);
  const rows = buildTopCommunicationDensityPolicy(mode);

  const hiddenBlocks = rows.filter((row) => isHidden(row.state)).length;
  const collapsedBlocks = rows.filter((row) => isCollapsed(row.state)).length;
  const dominantBlocks = rows.filter((row) => isDominant(row.state)).length;

  return {
    mode,
    totalBlocks: rows.length,
    hiddenBlocks,
    collapsedBlocks,
    dominantBlocks,
    contentDominant: rows.some(
      (row) => row.blockId === "content_stream" && row.state === "dominant",
    ),
    rows,
  };
}
