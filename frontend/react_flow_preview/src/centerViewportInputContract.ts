import type { ActiveDashboardRouteReadModel } from "./activeDashboardRouteReadModel.js";
import type { ChartViewKey } from "./chartTelemetryRegistry.js";
import type { GraphViewKey } from "./graphProjectionTypes.js";
import type { UnifiedVisualViewId } from "./unifiedVisualWorkspaceRegistry.js";

export type CenterViewportSurfaceKind = "graph" | "chart";

export type CenterViewportDrawerPolicy = "overlay_only";

export type CenterViewportRendererResponsibility = "render_only";

export type CenterViewportInputContract = {
  activeView: UnifiedVisualViewId;
  surfaceKind: CenterViewportSurfaceKind;
  activeGraphViewKey: GraphViewKey | null;
  activeChartViewKey: ChartViewKey | null;
  centerImmutable: true;
  drawerPolicy: CenterViewportDrawerPolicy;
  rendererResponsibility: CenterViewportRendererResponsibility;
  routingSource: "active_dashboard_route_read_model";
};

export function buildCenterViewportInputContract(
  route: ActiveDashboardRouteReadModel,
): CenterViewportInputContract {
  return {
    activeView: route.activeView,
    surfaceKind: route.activeKind,
    activeGraphViewKey: route.activeGraphViewKey,
    activeChartViewKey: route.activeChartViewKey,
    centerImmutable: true,
    drawerPolicy: "overlay_only",
    rendererResponsibility: "render_only",
    routingSource: "active_dashboard_route_read_model",
  };
}
