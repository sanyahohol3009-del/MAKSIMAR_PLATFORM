import type { LeftDrawerSection } from "./overlayDrawerLayoutContract.js";
import {
  getPermanentRailSelectionRouteBySurfaceId,
} from "./permanentRailActiveDashboardSelectionBinding.js";
import type {
  PermanentRailActiveDashboardSelectionRoute,
} from "./permanentRailActiveDashboardSelectionBinding.js";
import type { UnifiedVisualViewId } from "./unifiedVisualWorkspaceRegistry.js";

export type ActiveDashboardLeftDrawerBindingTarget =
  "active_dashboard_left_drawer_binding";

export type ActiveDashboardLeftDrawerBindingSource =
  "permanent_rail_active_dashboard_selection_binding";

export type ActiveDashboardLeftDrawerPanelKind =
  | "functions"
  | "settings"
  | "tools";

export type ActiveDashboardLeftDrawerInput = {
  activeSurfaceId: string;
  activeView: UnifiedVisualViewId;
};

export type ActiveDashboardLeftDrawerItem = {
  itemId: string;
  title: string;
  description: string;
  value: string;
  enabled: boolean;
  executable: false;
};

export type ActiveDashboardLeftDrawerSection = {
  sectionId: ActiveDashboardLeftDrawerPanelKind;
  leftDrawerSection: LeftDrawerSection;
  title: string;
  description: string;
  items: readonly ActiveDashboardLeftDrawerItem[];
};

export type ActiveDashboardLeftDrawerReadModel = {
  target: ActiveDashboardLeftDrawerBindingTarget;
  source: ActiveDashboardLeftDrawerBindingSource;
  activeSurfaceId: string;
  activeView: UnifiedVisualViewId;
  route: PermanentRailActiveDashboardSelectionRoute | null;
  routeReady: boolean;
  sections: readonly ActiveDashboardLeftDrawerSection[];
  totalSections: number;
  totalItems: number;
  permanentRailIsDashboardSelector: true;
  leftDrawerIsActiveDashboardContext: true;
  executableActionsAllowed: false;
  appTsxHardcodingAllowed: false;
};

export type ActiveDashboardLeftDrawerValidation = {
  valid: boolean;
  errors: readonly string[];
};

function buildItem(
  itemId: string,
  title: string,
  description: string,
  value: string,
  enabled = true,
): ActiveDashboardLeftDrawerItem {
  return {
    itemId,
    title,
    description,
    value,
    enabled,
    executable: false,
  };
}

function buildSections(
  route: PermanentRailActiveDashboardSelectionRoute | null,
  activeSurfaceId: string,
  activeView: UnifiedVisualViewId,
): readonly ActiveDashboardLeftDrawerSection[] {
  const routeStatus = route?.routeStatus ?? "center_viewport_not_ready";
  const rendererAdapterId = route?.rendererAdapterId ?? "not_connected";
  const rendererAdapterKind = route?.rendererAdapterKind ?? "not_connected";
  const dashboardTitle = route?.title ?? activeSurfaceId;

  return [
    {
      sectionId: "functions",
      leftDrawerSection: "visual_registry_navigation",
      title: "Functions",
      description: "Active dashboard functions and safe operator controls.",
      items: [
        buildItem(
          "active_dashboard_identity",
          "Active dashboard",
          "Currently selected dashboard from the permanent rail.",
          dashboardTitle,
        ),
        buildItem(
          "center_viewport_route",
          "Center viewport route",
          "Whether this dashboard has a registered center viewport route.",
          routeStatus,
          routeStatus === "center_viewport_ready",
        ),
        buildItem(
          "renderer_adapter",
          "Renderer adapter",
          "Adapter selected by dashboard skeleton route binding.",
          rendererAdapterId,
          rendererAdapterId !== "not_connected",
        ),
      ],
    },
    {
      sectionId: "settings",
      leftDrawerSection: "panel_navigation",
      title: "Settings",
      description: "Read-only settings for the selected dashboard shell route.",
      items: [
        buildItem(
          "surface_id",
          "Surface ID",
          "Canonical dashboard surface selected by permanent rail.",
          activeSurfaceId,
        ),
        buildItem(
          "active_view",
          "Active view",
          "Unified visual workspace view currently routed to center viewport.",
          activeView,
        ),
        buildItem(
          "renderer_kind",
          "Renderer kind",
          "Renderer family resolved by adapter boundary.",
          rendererAdapterKind,
          rendererAdapterKind !== "not_connected",
        ),
      ],
    },
    {
      sectionId: "tools",
      leftDrawerSection: "embedded_chat_context",
      title: "Tools",
      description: "Dashboard-specific tools reserved for future safe actions.",
      items: [
        buildItem(
          "safe_action_policy",
          "Safe action policy",
          "Drawer tools are currently read-only and non-executing.",
          "read_only",
        ),
        buildItem(
          "manual_hardcoding_policy",
          "Manual hardcoding policy",
          "Dashboard buttons and routes must remain registry/read-model driven.",
          "forbidden",
        ),
        buildItem(
          "future_data_binding",
          "Future data binding",
          "Real metrics, topology, memory and diagnostics bind after skeleton stabilization.",
          "pending",
        ),
      ],
    },
  ];
}

export function buildActiveDashboardLeftDrawerReadModel(
  input: ActiveDashboardLeftDrawerInput,
): ActiveDashboardLeftDrawerReadModel {
  const route = getPermanentRailSelectionRouteBySurfaceId(input.activeSurfaceId);
  const sections = buildSections(route, input.activeSurfaceId, input.activeView);

  return {
    target: "active_dashboard_left_drawer_binding",
    source: "permanent_rail_active_dashboard_selection_binding",
    activeSurfaceId: input.activeSurfaceId,
    activeView: input.activeView,
    route,
    routeReady: route?.routeStatus === "center_viewport_ready",
    sections,
    totalSections: sections.length,
    totalItems: sections.reduce((total, section) => total + section.items.length, 0),
    permanentRailIsDashboardSelector: true,
    leftDrawerIsActiveDashboardContext: true,
    executableActionsAllowed: false,
    appTsxHardcodingAllowed: false,
  };
}

export function getActiveDashboardLeftDrawerSectionByAlias(
  readModel: ActiveDashboardLeftDrawerReadModel,
  leftDrawerSection: LeftDrawerSection,
): ActiveDashboardLeftDrawerSection {
  const matchedSection = readModel.sections.find(
    (section) => section.leftDrawerSection === leftDrawerSection,
  );

  if (matchedSection) {
    return matchedSection;
  }

  const fallbackSection = readModel.sections[0];

  if (!fallbackSection) {
    throw new Error("active_dashboard_left_drawer_sections_empty");
  }

  return fallbackSection;
}

export function validateActiveDashboardLeftDrawerReadModel(
  readModel: ActiveDashboardLeftDrawerReadModel,
): ActiveDashboardLeftDrawerValidation {
  const errors: string[] = [];
  const seenSections = new Set<string>();
  const seenItems = new Set<string>();

  if (readModel.target !== "active_dashboard_left_drawer_binding") {
    errors.push("target_must_be_active_dashboard_left_drawer_binding");
  }

  if (readModel.source !== "permanent_rail_active_dashboard_selection_binding") {
    errors.push("source_must_be_permanent_rail_active_dashboard_selection_binding");
  }

  if (readModel.totalSections !== 3) {
    errors.push("total_sections_must_be_3");
  }

  if (readModel.totalItems < 1) {
    errors.push("total_items_must_be_positive");
  }

  if (!readModel.permanentRailIsDashboardSelector) {
    errors.push("permanent_rail_must_remain_dashboard_selector");
  }

  if (!readModel.leftDrawerIsActiveDashboardContext) {
    errors.push("left_drawer_must_be_active_dashboard_context");
  }

  if (readModel.executableActionsAllowed) {
    errors.push("left_drawer_actions_must_remain_non_executing");
  }

  if (readModel.appTsxHardcodingAllowed) {
    errors.push("app_tsx_hardcoding_forbidden");
  }

  for (const section of readModel.sections) {
    if (seenSections.has(section.sectionId)) {
      errors.push(`duplicate_section:${section.sectionId}`);
    }

    seenSections.add(section.sectionId);

    if (section.items.length === 0) {
      errors.push(`empty_section:${section.sectionId}`);
    }

    for (const item of section.items) {
      if (seenItems.has(item.itemId)) {
        errors.push(`duplicate_item:${item.itemId}`);
      }

      seenItems.add(item.itemId);

      if (item.executable) {
        errors.push(`item_must_not_be_executable:${item.itemId}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
