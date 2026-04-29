import {
  getActiveViewForPermanentRailSurfaceId,
} from "./permanentRailActiveDashboardSelectionBinding.js";
import {
  getUnifiedVisualWorkspaceRegistryEntry,
  type UnifiedVisualViewId,
} from "./unifiedVisualWorkspaceRegistry.js";

export type ActiveDashboardCenterViewportBindingTarget =
  "active_dashboard_center_viewport_binding";

export type ActiveDashboardCenterViewportBindingReadModel = {
  target: ActiveDashboardCenterViewportBindingTarget;
  surfaceId: string;
  viewId: UnifiedVisualViewId | null;
  resolved: boolean;
  registryResolved: boolean;
  hardcodedRendererAllowed: false;
};

export function resolveCenterViewportForSurface(
  surfaceId: string,
): ActiveDashboardCenterViewportBindingReadModel {
  const viewId = getActiveViewForPermanentRailSurfaceId(surfaceId);

  if (!viewId) {
    return {
      target: "active_dashboard_center_viewport_binding",
      surfaceId,
      viewId: null,
      resolved: false,
      registryResolved: false,
      hardcodedRendererAllowed: false,
    };
  }

  try {
    getUnifiedVisualWorkspaceRegistryEntry(viewId);

    return {
      target: "active_dashboard_center_viewport_binding",
      surfaceId,
      viewId,
      resolved: true,
      registryResolved: true,
      hardcodedRendererAllowed: false,
    };
  } catch {
    return {
      target: "active_dashboard_center_viewport_binding",
      surfaceId,
      viewId: null,
      resolved: false,
      registryResolved: false,
      hardcodedRendererAllowed: false,
    };
  }
}
