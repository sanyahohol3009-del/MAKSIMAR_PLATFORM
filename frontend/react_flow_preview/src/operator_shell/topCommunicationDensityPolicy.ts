export type TopCommunicationBlockId =
  | "section_tabs"
  | "surface_selector"
  | "summary_chip_lane"
  | "content_stream"
  | "support_meta";

export type TopCommunicationLane =
  | "header"
  | "subheader"
  | "content";

export type TopCommunicationBlockState =
  | "hidden"
  | "collapsed"
  | "visible"
  | "dominant";

export type TopCommunicationDensityMode =
  | "baseline_density"
  | "normalized_density";

export type TopCommunicationDensityPolicyEntry = {
  blockId: TopCommunicationBlockId;
  title: string;
  lane: TopCommunicationLane;
  state: TopCommunicationBlockState;
  priority: 1 | 2 | 3;
  notes: string;
};

function buildBaselineDensityPolicy():
  readonly TopCommunicationDensityPolicyEntry[] {
  return [
    {
      blockId: "section_tabs",
      title: "Section Tabs",
      lane: "header",
      state: "visible",
      priority: 1,
      notes: "Primary section switching remains visible in baseline mode.",
    },
    {
      blockId: "surface_selector",
      title: "Surface Selector",
      lane: "header",
      state: "visible",
      priority: 2,
      notes: "Surface exposure selector is visible in baseline mode.",
    },
    {
      blockId: "summary_chip_lane",
      title: "Summary Chip Lane",
      lane: "subheader",
      state: "visible",
      priority: 2,
      notes: "Summary chips are visible in baseline mode.",
    },
    {
      blockId: "content_stream",
      title: "Content Stream",
      lane: "content",
      state: "visible",
      priority: 1,
      notes: "Content stream is visible but not yet dominant in baseline mode.",
    },
    {
      blockId: "support_meta",
      title: "Support Meta",
      lane: "subheader",
      state: "visible",
      priority: 3,
      notes: "Support metadata remains visible in baseline mode.",
    },
  ];
}

function buildNormalizedDensityPolicy():
  readonly TopCommunicationDensityPolicyEntry[] {
  return [
    {
      blockId: "section_tabs",
      title: "Section Tabs",
      lane: "header",
      state: "visible",
      priority: 1,
      notes: "Section tabs remain visible in normalized fullscreen communication mode.",
    },
    {
      blockId: "surface_selector",
      title: "Surface Selector",
      lane: "header",
      state: "collapsed",
      priority: 2,
      notes: "Surface selector remains available but should not dominate the header.",
    },
    {
      blockId: "summary_chip_lane",
      title: "Summary Chip Lane",
      lane: "subheader",
      state: "collapsed",
      priority: 2,
      notes: "Summary chips are reduced to avoid communication clutter.",
    },
    {
      blockId: "content_stream",
      title: "Content Stream",
      lane: "content",
      state: "dominant",
      priority: 1,
      notes: "Content stream becomes the primary visual block in fullscreen communication.",
    },
    {
      blockId: "support_meta",
      title: "Support Meta",
      lane: "subheader",
      state: "hidden",
      priority: 3,
      notes: "Support metadata is hidden to reduce communication density.",
    },
  ];
}

export function buildTopCommunicationDensityPolicy(
  mode: TopCommunicationDensityMode,
): readonly TopCommunicationDensityPolicyEntry[] {
  switch (mode) {
    case "baseline_density":
      return buildBaselineDensityPolicy();
    case "normalized_density":
      return buildNormalizedDensityPolicy();
  }
}
