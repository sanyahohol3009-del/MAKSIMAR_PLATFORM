import {
  resolveCenterViewportForSurface,
} from "./activeDashboardCenterViewportBinding.js";

import {
  buildActiveDashboardRouteReadModel,
} from "./activeDashboardRouteReadModel.js";

import {
  buildCenterViewportInputContract,
} from "./centerViewportInputContract.js";

import {
  graphProjectionRegistry,
} from "./graphProjectionData.js";

import {
  buildChartOption,
} from "./chartTelemetrySemantics.js";

export type ActiveDashboardCenterRendererKind =
  | "react_flow_graph_renderer"
  | "echarts_chart_renderer"
  | "not_ready";

export type ActiveDashboardCenterRendererBindingReadModel = {
  surfaceId: string;
  resolved: boolean;
  rendererKind: ActiveDashboardCenterRendererKind;
  viewId: string | null;
  graphNodeCount: number;
  graphEdgeCount: number;
  chartOptionAvailable: boolean;
  usesExistingCenterDashboardViewport: true;
  newRendererCreated: false;
  appTsxHardcodingAllowed: false;
};

export function buildActiveDashboardCenterRendererBinding(
  surfaceId: string,
): ActiveDashboardCenterRendererBindingReadModel {
  const center = resolveCenterViewportForSurface(surfaceId);

  if (!center.resolved || !center.viewId) {
    return {
      surfaceId,
      resolved: false,
      rendererKind: "not_ready",
      viewId: null,
      graphNodeCount: 0,
      graphEdgeCount: 0,
      chartOptionAvailable: false,
      usesExistingCenterDashboardViewport: true,
      newRendererCreated: false,
      appTsxHardcodingAllowed: false,
    };
  }

  const route = buildActiveDashboardRouteReadModel(center.viewId);
  const input = buildCenterViewportInputContract(route);

  // GRAPH (ReactFlow)
  if (input.activeGraphViewKey) {
    const graph = graphProjectionRegistry[input.activeGraphViewKey];

    return {
      surfaceId,
      resolved: true,
      rendererKind: "react_flow_graph_renderer",
      viewId: center.viewId,
      graphNodeCount: graph.nodes.length,
      graphEdgeCount: graph.edges.length,
      chartOptionAvailable: false,
      usesExistingCenterDashboardViewport: true,
      newRendererCreated: false,
      appTsxHardcodingAllowed: false,
    };
  }

  // CHART (ECharts)
  if (input.activeChartViewKey) {
    const option = buildChartOption(input.activeChartViewKey);

    return {
      surfaceId,
      resolved: true,
      rendererKind: "echarts_chart_renderer",
      viewId: center.viewId,
      graphNodeCount: 0,
      graphEdgeCount: 0,
      chartOptionAvailable: option !== null,
      usesExistingCenterDashboardViewport: true,
      newRendererCreated: false,
      appTsxHardcodingAllowed: false,
    };
  }

  return {
    surfaceId,
    resolved: false,
    rendererKind: "not_ready",
    viewId: center.viewId,
    graphNodeCount: 0,
    graphEdgeCount: 0,
    chartOptionAvailable: false,
    usesExistingCenterDashboardViewport: true,
    newRendererCreated: false,
    appTsxHardcodingAllowed: false,
  };
}
