export type OperatorZoneId =
  | "top_communication"
  | "left_navigation"
  | "right_context"
  | "center_scene"
  | "bottom_footer";

export type OperatorShellMode =
  | "baseline"
  | "communication_focus"
  | "left_navigation_focus"
  | "right_context_focus";

export type OperatorZoneVisibilityState =
  | "hidden"
  | "collapsed_strip"
  | "drawer_overlay"
  | "fullscreen_overlay"
  | "always_visible";

export type OperatorZonePolicyEntry = {
  zoneId: OperatorZoneId;
  title: string;
  visibilityState: OperatorZoneVisibilityState;
  interactive: boolean;
  overlay: boolean;
  centerImmutable: boolean;
  notes: string;
};

function buildBaselinePolicy(): readonly OperatorZonePolicyEntry[] {
  return [
    {
      zoneId: "top_communication",
      title: "Top Communication",
      visibilityState: "collapsed_strip",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Collapsed communication strip remains visible in baseline mode.",
    },
    {
      zoneId: "left_navigation",
      title: "Left Navigation",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Left navigation drawer is hidden until explicitly opened.",
    },
    {
      zoneId: "right_context",
      title: "Right Context",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Right inspect/context drawer is hidden until explicitly opened.",
    },
    {
      zoneId: "center_scene",
      title: "Center Scene",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Center visual scene remains the primary immutable display surface.",
    },
    {
      zoneId: "bottom_footer",
      title: "Bottom Footer",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Footer/status lane stays outside the center scene.",
    },
  ];
}

function buildCommunicationFocusPolicy(): readonly OperatorZonePolicyEntry[] {
  return [
    {
      zoneId: "top_communication",
      title: "Top Communication",
      visibilityState: "fullscreen_overlay",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Communication surface expands to fullscreen overlay inside the shell.",
    },
    {
      zoneId: "left_navigation",
      title: "Left Navigation",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Left navigation is suppressed while communication is fullscreen.",
    },
    {
      zoneId: "right_context",
      title: "Right Context",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Right inspect/context is suppressed while communication is fullscreen.",
    },
    {
      zoneId: "center_scene",
      title: "Center Scene",
      visibilityState: "always_visible",
      interactive: false,
      overlay: false,
      centerImmutable: true,
      notes: "Center scene remains underneath overlay and must not be resized.",
    },
    {
      zoneId: "bottom_footer",
      title: "Bottom Footer",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Footer/status lane remains outside the communication overlay.",
    },
  ];
}

function buildLeftNavigationFocusPolicy(): readonly OperatorZonePolicyEntry[] {
  return [
    {
      zoneId: "top_communication",
      title: "Top Communication",
      visibilityState: "collapsed_strip",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Top communication remains collapsed while left navigation is open.",
    },
    {
      zoneId: "left_navigation",
      title: "Left Navigation",
      visibilityState: "drawer_overlay",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Left drawer opens as overlay navigation surface.",
    },
    {
      zoneId: "right_context",
      title: "Right Context",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Right drawer stays hidden during left-navigation focus.",
    },
    {
      zoneId: "center_scene",
      title: "Center Scene",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Center scene remains primary behind left overlay drawer.",
    },
    {
      zoneId: "bottom_footer",
      title: "Bottom Footer",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Footer remains visible in navigation focus.",
    },
  ];
}

function buildRightContextFocusPolicy(): readonly OperatorZonePolicyEntry[] {
  return [
    {
      zoneId: "top_communication",
      title: "Top Communication",
      visibilityState: "collapsed_strip",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Top communication remains collapsed while right context is open.",
    },
    {
      zoneId: "left_navigation",
      title: "Left Navigation",
      visibilityState: "hidden",
      interactive: false,
      overlay: true,
      centerImmutable: true,
      notes: "Left drawer stays hidden during right-context focus.",
    },
    {
      zoneId: "right_context",
      title: "Right Context",
      visibilityState: "drawer_overlay",
      interactive: true,
      overlay: true,
      centerImmutable: true,
      notes: "Right drawer opens as inspect/context overlay surface.",
    },
    {
      zoneId: "center_scene",
      title: "Center Scene",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Center scene remains primary behind right overlay drawer.",
    },
    {
      zoneId: "bottom_footer",
      title: "Bottom Footer",
      visibilityState: "always_visible",
      interactive: true,
      overlay: false,
      centerImmutable: true,
      notes: "Footer remains visible in context focus.",
    },
  ];
}

export function buildOperatorZoneVisibilityPolicy(
  shellMode: OperatorShellMode,
): readonly OperatorZonePolicyEntry[] {
  switch (shellMode) {
    case "baseline":
      return buildBaselinePolicy();
    case "communication_focus":
      return buildCommunicationFocusPolicy();
    case "left_navigation_focus":
      return buildLeftNavigationFocusPolicy();
    case "right_context_focus":
      return buildRightContextFocusPolicy();
  }
}
