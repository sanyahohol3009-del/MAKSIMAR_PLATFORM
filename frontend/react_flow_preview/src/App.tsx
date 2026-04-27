import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { graphProjectionRegistry } from "./graphProjectionData.js";
import {
  buildStyledEdges,
  buildStyledNodes,
} from "./graphVisualSemantics.js";
import {
  buildUnifiedVisualInspectPresentation,
  type SelectedGraphInspectItem,
} from "./unifiedVisualInspectSemantics.js";
import { buildUnifiedVisualWorkspaceSnapshot } from "./unifiedVisualWorkspace.js";
import {
  getUnifiedVisualWorkspaceRegistryEntry,
  type UnifiedVisualViewId,
} from "./unifiedVisualWorkspaceRegistry.js";
import { buildChartOption } from "./chartTelemetrySemantics.js";
import type { ChartViewKey } from "./chartTelemetryRegistry.js";
import type {
  GraphViewKey,
  ProjectionEdgeRecord,
  ProjectionNodeRecord,
} from "./graphProjectionTypes.js";

import { buildMemoryKnowledgeShellReadModel } from "./memoryKnowledgeShellReadModel.js";
import type { MemoryKnowledgeExposureKey } from "./memoryKnowledgeExposureRegistry.js";

import { buildPanelNavigationReadModel } from "./panelNavigationReadModel.js";
import type { PanelNavigationPanelId } from "./panelNavigationRegistry.js";

import { buildPanelFamilyTaxonomyExposureReadModel } from "./panelFamilyTaxonomyExposureReadModel.js";
import { buildPanelFamilyTaxonomyExposureInspectPresentation } from "./panelFamilyTaxonomyExposureInspect.js";
import type { PanelTaxonomyPanelId } from "./panelFamilyTaxonomyExposureRegistry.js";

import {
  buildOverlayDrawerLayoutContract,
  type LeftDrawerSection,
  type RightDrawerSection,
} from "./overlayDrawerLayoutContract.js";
import {
  buildInitialOverlayDrawerShellState,
  toggleOverlayDrawerMode,
} from "./overlayDrawerShellState.js";

import {
  buildJarvisChatDrawerContract,
  type JarvisChatDrawerSectionId,
} from "./jarvis_chat/jarvisChatDrawerContract.js";
import { buildJarvisChatDrawerFixture } from "./jarvis_chat/jarvisChatDrawerFixture.js";
import { buildJarvisChatDrawerReadModel } from "./jarvis_chat/jarvisChatDrawerReadModel.js";

import { buildEmbeddedChatShellExposureReadModel } from "./jarvis_chat/embeddedChatShellExposureReadModel.js";
import { buildEmbeddedChatShellExposureInspectPresentation } from "./jarvis_chat/embeddedChatShellExposureInspect.js";
import type { EmbeddedChatSurfaceId } from "./jarvis_chat/embeddedChatSurfaceRegistry.js";

import { buildOperatorZoneAppBinding } from "./operator_shell/operatorZoneAppBinding.js";
import { buildTopCommunicationDensityAppBinding } from "./operator_shell/topCommunicationDensityAppBinding.js";

import { TopChatDrawer } from "./shell/TopChatDrawer.js";
import { SummaryCardsOverlay } from "./shell/SummaryCardsOverlay.js";
import { TopStatusStrip } from "./shell/TopStatusStrip.js";
import { LeftDashboardDrawer } from "./shell/LeftDashboardDrawer.js";

import { ChatConversationPane } from "./features/chat/ChatConversationPane.js";
import { ChatInputBar } from "./features/chat/ChatInputBar.js";
import { ChatSidebar } from "./features/chat/ChatSidebar.js";
import { ChatDrawerBody } from "./features/chat/ChatDrawerBody.js";

type ChartInstanceLike = {
  dispose: () => void;
  resize: () => void;
  setOption: (option: unknown, notMerge?: boolean) => void;
};

type InspectPresentationLike = {
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

function isGraphViewId(
  viewId: UnifiedVisualViewId,
): viewId is `graph:${GraphViewKey}` {
  return viewId.startsWith("graph:");
}

function isChartViewId(
  viewId: UnifiedVisualViewId,
): viewId is `chart:${ChartViewKey}` {
  return viewId.startsWith("chart:");
}

function extractGraphViewKey(viewId: `graph:${GraphViewKey}`): GraphViewKey {
  return viewId.slice("graph:".length) as GraphViewKey;
}

function extractChartViewKey(viewId: `chart:${ChartViewKey}`): ChartViewKey {
  return viewId.slice("chart:".length) as ChartViewKey;
}

function getLeftSectionTitle(section: LeftDrawerSection): string {
  switch (section) {
    case "visual_registry_navigation":
      return "Visual Registry";
    case "panel_navigation":
      return "Panel Navigation";
    case "embedded_chat_context":
      return "Embedded Chat Context";
  }
}

function getRightSectionTitle(section: RightDrawerSection): string {
  switch (section) {
    case "inspect":
      return "Inspect";
    case "memory_knowledge":
      return "Memory / Knowledge";
    case "panel_family_taxonomy_exposure":
      return "Family / Taxonomy / Exposure";
    case "panel_navigation":
      return "Panel Navigation";
    case "embedded_chat_context":
      return "Embedded Chat Context";
  }
}

function getJarvisChatSectionTitle(
  section: JarvisChatDrawerSectionId,
): string {
  switch (section) {
    case "conversation":
      return "Conversation";
    case "project_context":
      return "Project Context";
    case "command_handoff":
      return "Command Handoff";
    case "diagnostics":
      return "Diagnostics";
  }
}

function getPreferredJarvisSection(
  surfaceId: EmbeddedChatSurfaceId,
): JarvisChatDrawerSectionId {
  switch (surfaceId) {
    case "project_context_host":
      return "project_context";
    case "conversation_history_lane":
      return "conversation";
    case "code_output_lane":
      return "conversation";
    case "command_support_lane":
      return "command_handoff";
  }
}

function normalizeOperatorZoneDrawerMode(
  mode: "hidden" | "peek" | "expanded",
): "hidden" | "expanded" {
  return mode === "expanded" ? "expanded" : "hidden";
}

export default function App() {
  const overlayLayoutContract = buildOverlayDrawerLayoutContract();
  const jarvisChatDrawerContract = buildJarvisChatDrawerContract();
  const jarvisChatDrawerFixture = buildJarvisChatDrawerFixture();
  const jarvisChatDrawerReadModel = buildJarvisChatDrawerReadModel();
  const embeddedChatShellExposureReadModel =
    buildEmbeddedChatShellExposureReadModel();

  const leftDrawerSections: LeftDrawerSection[] = [
    "visual_registry_navigation",
    "panel_navigation",
    "embedded_chat_context",
  ];

  const rightDrawerSections: RightDrawerSection[] = [
    "inspect",
    "memory_knowledge",
    "panel_family_taxonomy_exposure",
  ];

  const [drawerShellState, setDrawerShellState] = useState(
    buildInitialOverlayDrawerShellState(),
  );

  const [activeView, setActiveView] =
    useState<UnifiedVisualViewId>("graph:topology");
  const [selectedItem, setSelectedItem] =
    useState<SelectedGraphInspectItem | null>(null);

  const [activeMemoryExposure, setActiveMemoryExposure] =
    useState<MemoryKnowledgeExposureKey>("memory_registry_summary");
  const [activePanelNavigation, setActivePanelNavigation] =
    useState<PanelNavigationPanelId>("system_status");
  const [activePanelTaxonomyExposure, setActivePanelTaxonomyExposure] =
    useState<PanelTaxonomyPanelId>("system_status");
  const [activeJarvisChatSection, setActiveJarvisChatSection] =
    useState<JarvisChatDrawerSectionId>("conversation");
  const [activeEmbeddedChatSurface, setActiveEmbeddedChatSurface] =
    useState<EmbeddedChatSurfaceId>("project_context_host");

  const chartHostRef = useRef<HTMLDivElement | null>(null);
  const chartInstanceRef = useRef<ChartInstanceLike | null>(null);
  const chartResizeHandlerRef = useRef<(() => void) | null>(null);

  const activeEntry = getUnifiedVisualWorkspaceRegistryEntry(activeView);
  const workspaceSnapshot = buildUnifiedVisualWorkspaceSnapshot(activeView);

  const memoryKnowledgeShell =
    buildMemoryKnowledgeShellReadModel(activeMemoryExposure);

  const panelNavigationReadModel = buildPanelNavigationReadModel();

  const panelFamilyTaxonomyExposureReadModel =
    buildPanelFamilyTaxonomyExposureReadModel();
  const panelFamilyTaxonomyExposureInspect =
    buildPanelFamilyTaxonomyExposureInspectPresentation(
      activePanelTaxonomyExposure,
    );

  const embeddedChatShellExposureInspect =
    buildEmbeddedChatShellExposureInspectPresentation(
      activeEmbeddedChatSurface,
    );

  const topDrawerExposureGroup =
    embeddedChatShellExposureReadModel.groupedExposure.find(
      (group) => group.target === "top_drawer_primary",
    ) ?? null;

  const leftReferenceExposureGroup =
    embeddedChatShellExposureReadModel.groupedExposure.find(
      (group) => group.target === "left_drawer_context_reference",
    ) ?? null;

  const rightReferenceExposureGroup =
    embeddedChatShellExposureReadModel.groupedExposure.find(
      (group) => group.target === "right_drawer_inspect_reference",
    ) ?? null;

  const activeGraphViewKey = isGraphViewId(activeView)
    ? extractGraphViewKey(activeView)
    : null;

  const activeChartViewKey = isChartViewId(activeView)
    ? extractChartViewKey(activeView)
    : null;

  const currentGraphView = activeGraphViewKey
    ? graphProjectionRegistry[activeGraphViewKey]
    : null;

  const nodes = useMemo(
    () => (activeGraphViewKey ? buildStyledNodes(activeGraphViewKey) : []),
    [activeGraphViewKey],
  );

  const edges = useMemo(
    () => (activeGraphViewKey ? buildStyledEdges(activeGraphViewKey) : []),
    [activeGraphViewKey],
  );

  const selectedNodeMap = useMemo(() => {
    if (!currentGraphView) {
      return new Map<string, ProjectionNodeRecord>();
    }
    return new Map(currentGraphView.nodes.map((node) => [node.id, node]));
  }, [currentGraphView]);

  const selectedEdgeMap = useMemo(() => {
    if (!currentGraphView) {
      return new Map<string, ProjectionEdgeRecord>();
    }
    return new Map(currentGraphView.edges.map((edge) => [edge.id, edge]));
  }, [currentGraphView]);

  const inspectPresentation = buildUnifiedVisualInspectPresentation(
    activeView,
    selectedItem,
  );

  const chartOption = useMemo(
    () => (activeChartViewKey ? buildChartOption(activeChartViewKey) : null),
    [activeChartViewKey],
  );

  const diagnosticsMessages = jarvisChatDrawerFixture.messages.filter(
    (message) => message.sourceScope === "diagnostics",
  );

  const topStripHeight = 42;
  const mainVisualHeight = "78vh";

  const presenceItems = ["home_001", "dev_001", "mobile_001"];

  const activeEmbeddedChatSurfaceLabel =
    topDrawerExposureGroup?.rows.find(
      (row) => row.surfaceId === activeEmbeddedChatSurface,
    )?.title ?? activeEmbeddedChatSurface;

  const operatorZoneAppBinding = buildOperatorZoneAppBinding({
    topMode: normalizeOperatorZoneDrawerMode(drawerShellState.topMode),
    leftMode: normalizeOperatorZoneDrawerMode(drawerShellState.leftMode),
    rightMode: normalizeOperatorZoneDrawerMode(drawerShellState.rightMode),
  });

  const topCommunicationDensityAppBinding =
    buildTopCommunicationDensityAppBinding({
      fullscreenCommunication:
        operatorZoneAppBinding.shellMode === "communication_focus",
    });

  const disposeChartRuntime = () => {
    if (chartResizeHandlerRef.current) {
      window.removeEventListener("resize", chartResizeHandlerRef.current);
      chartResizeHandlerRef.current = null;
    }

    if (chartInstanceRef.current) {
      chartInstanceRef.current.dispose();
      chartInstanceRef.current = null;
    }

    if (chartHostRef.current) {
      chartHostRef.current.innerHTML = "";
    }
  };

  useEffect(() => {
    if (!activeChartViewKey || !chartOption) {
      disposeChartRuntime();
      return;
    }

    let cancelled = false;
    let rafId: number | null = null;

    const setupChart = async () => {
      const echarts = await import("echarts");

      if (cancelled) {
        return;
      }

      const host = chartHostRef.current;
      if (!host) {
        return;
      }

      disposeChartRuntime();

      rafId = window.requestAnimationFrame(() => {
        if (cancelled || !chartHostRef.current) {
          return;
        }

        const instance = echarts.init(chartHostRef.current);
        chartInstanceRef.current = instance as unknown as ChartInstanceLike;
        instance.setOption(chartOption, true);

        const onResize = () => {
          chartInstanceRef.current?.resize();
        };

        chartResizeHandlerRef.current = onResize;
        window.addEventListener("resize", onResize);
        instance.resize();
      });
    };

    void setupChart();

    return () => {
      cancelled = true;

      if (rafId !== null) {
        window.cancelAnimationFrame(rafId);
      }

      disposeChartRuntime();
    };
  }, [activeChartViewKey, chartOption]);

  const goToView = (viewId: UnifiedVisualViewId) => {
    setActiveView(viewId);
    setSelectedItem(null);
  };

  const toggleLeftDrawer = () => {
    setDrawerShellState((current) => {
      const nextLeftMode = toggleOverlayDrawerMode(current.leftMode);

      return {
        ...current,
        leftMode: nextLeftMode,
        rightMode: nextLeftMode === "expanded" ? "hidden" : current.rightMode,
      };
    });
  };

  const toggleRightDrawer = () => {
    setDrawerShellState((current) => {
      const nextRightMode = toggleOverlayDrawerMode(current.rightMode);

      return {
        ...current,
        rightMode: nextRightMode,
        leftMode: nextRightMode === "expanded" ? "hidden" : current.leftMode,
      };
    });
  };

  const toggleTopDrawer = () => {
    setDrawerShellState((current) => ({
      ...current,
      topMode: toggleOverlayDrawerMode(current.topMode),
    }));
  };

  const activateEmbeddedChatSurface = (surfaceId: EmbeddedChatSurfaceId) => {
    setActiveEmbeddedChatSurface(surfaceId);
    setActiveJarvisChatSection(getPreferredJarvisSection(surfaceId));
  };

  const renderPresentation = (
    presentation: InspectPresentationLike,
  ) => (
    <>
      <div
        style={{
          display: "flex",
          gap: 8,
          flexWrap: "wrap",
          marginBottom: 12,
        }}
      >
        <span className="inspect-chip">{presentation.semanticKind}</span>
      </div>

      <div className="inspect-explanation">
        <h3>{presentation.title}</h3>
        <p>{presentation.explanation}</p>
      </div>

      <div className="inspect-sections">
        {presentation.sections.map((section) => (
          <section key={section.title} className="inspect-section">
            <h3>{section.title}</h3>
            <div className="inspect-fields">
              {section.items.map((item) => (
                <div
                  key={`${section.title}:${item.key}`}
                  className="inspect-field"
                >
                  <span className="inspect-field-key">{item.key}</span>
                  <span className="inspect-field-value">{item.value}</span>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </>
  );

  const renderLeftDrawerBody = () => {
    switch (drawerShellState.activeLeftSection) {
      case "visual_registry_navigation":
        return (
          <div className="workspace-sidebar-groups">
            {workspaceSnapshot.groupedViews.map((group) => (
              <section key={group.group} className="workspace-sidebar-group">
                <h3>{group.title}</h3>
                <div className="workspace-sidebar-items">
                  {group.views.map((view) => (
                    <button
                      key={view.viewId}
                      type="button"
                      className={
                        view.viewId === activeView
                          ? "workspace-sidebar-item active"
                          : "workspace-sidebar-item"
                      }
                      onClick={() => goToView(view.viewId)}
                    >
                      <span className="workspace-sidebar-item-title">
                        {view.title}
                      </span>
                      <span className="workspace-sidebar-item-meta">
                        {view.viewKind} · {view.summaryLabel}: {view.summaryValue}
                      </span>
                    </button>
                  ))}
                </div>
              </section>
            ))}
          </div>
        );

      case "panel_navigation":
        return (
          <div className="workspace-sidebar-groups">
            {panelNavigationReadModel.groupedNavigation.map((group) => (
              <section
                key={group.navigationViewId}
                className="workspace-sidebar-group"
              >
                <h3>{group.title}</h3>
                <div className="workspace-sidebar-items">
                  {group.rows.map((row) => (
                    <button
                      key={row.panelId}
                      type="button"
                      className={
                        row.panelId === activePanelNavigation
                          ? "workspace-sidebar-item active"
                          : "workspace-sidebar-item"
                      }
                      onClick={() => setActivePanelNavigation(row.panelId)}
                    >
                      <span className="workspace-sidebar-item-title">
                        {row.title}
                      </span>
                      <span className="workspace-sidebar-item-meta">
                        {row.workspaceRole} · {row.workspaceId}
                      </span>
                    </button>
                  ))}
                </div>
              </section>
            ))}
          </div>
        );

      case "embedded_chat_context":
        return (
          <div className="workspace-sidebar-groups">
            <section className="workspace-sidebar-group">
              <h3>Left Reference Exposure</h3>
              <div className="workspace-sidebar-items">
                {leftReferenceExposureGroup?.rows.map((row) => (
                  <button
                    key={row.surfaceId}
                    type="button"
                    className={
                      row.surfaceId === activeEmbeddedChatSurface
                        ? "workspace-sidebar-item active"
                        : "workspace-sidebar-item"
                    }
                    onClick={() => activateEmbeddedChatSurface(row.surfaceId)}
                  >
                    <span className="workspace-sidebar-item-title">
                      {row.title}
                    </span>
                    <span className="workspace-sidebar-item-meta">
                      {row.targetSection} · {row.countLabel}: {row.countValue}
                    </span>
                  </button>
                )) ?? null}
              </div>
            </section>

            <section className="workspace-sidebar-group">
              <h3>Exposure Inspect</h3>
              {renderPresentation(embeddedChatShellExposureInspect)}
            </section>
          </div>
        );
    }
  };

  const renderRightDrawerBody = () => {
    switch (drawerShellState.activeRightSection) {
      case "memory_knowledge":
        return (
          <>
            <div className="view-switcher-group-shell">
              {memoryKnowledgeShell.snapshot.groupedEntries.map((group) => (
                <section
                  key={group.targetSurface}
                  className="view-switcher-group"
                >
                  <div className="view-switcher-group-title">{group.title}</div>
                  <div
                    className="view-switcher"
                    style={{
                      display: "flex",
                      flexWrap: "nowrap",
                      overflowX: "auto",
                      gap: 8,
                    }}
                  >
                    {group.entries.map((entry) => (
                      <button
                        key={entry.exposureKey}
                        type="button"
                        className={
                          entry.exposureKey === activeMemoryExposure
                            ? "view-switch-button active"
                            : "view-switch-button"
                        }
                        onClick={() => setActiveMemoryExposure(entry.exposureKey)}
                      >
                        {entry.title}
                      </button>
                    ))}
                  </div>
                </section>
              ))}
            </div>
            {renderPresentation(memoryKnowledgeShell.activeInspect)}
          </>
        );

      case "panel_family_taxonomy_exposure":
        return (
          <>
            <div className="view-switcher-group-shell">
              {panelFamilyTaxonomyExposureReadModel.groupedTaxonomy.map((group) => (
                <section
                  key={group.shellTaxonomy}
                  className="view-switcher-group"
                >
                  <div className="view-switcher-group-title">{group.title}</div>
                  <div
                    className="view-switcher"
                    style={{
                      display: "flex",
                      flexWrap: "nowrap",
                      overflowX: "auto",
                      gap: 8,
                    }}
                  >
                    {group.rows.map((row) => (
                      <button
                        key={row.panelId}
                        type="button"
                        className={
                          row.panelId === activePanelTaxonomyExposure
                            ? "view-switch-button active"
                            : "view-switch-button"
                        }
                        onClick={() => setActivePanelTaxonomyExposure(row.panelId)}
                      >
                        {row.title}
                      </button>
                    ))}
                  </div>
                </section>
              ))}
            </div>
            {renderPresentation(panelFamilyTaxonomyExposureInspect)}
          </>
        );

      case "inspect":
      default:
        return (
          <>
            {renderPresentation(inspectPresentation)}

            {rightReferenceExposureGroup?.rows.length ? (
              <section className="inspect-section" style={{ marginTop: 16 }}>
                <h3>Embedded Chat References</h3>

                <div
                  style={{
                    display: "flex",
                    gap: 8,
                    flexWrap: "nowrap",
                    overflowX: "auto",
                    marginBottom: 12,
                  }}
                >
                  {rightReferenceExposureGroup.rows.map((row) => (
                    <button
                      key={row.surfaceId}
                      type="button"
                      className={
                        row.surfaceId === activeEmbeddedChatSurface
                          ? "view-switch-button active"
                          : "view-switch-button"
                      }
                      onClick={() => activateEmbeddedChatSurface(row.surfaceId)}
                    >
                      {row.title}
                    </button>
                  ))}
                </div>

                {renderPresentation(embeddedChatShellExposureInspect)}
              </section>
            ) : null}
          </>
        );
    }
  };

  const renderTopDrawerBody = () => (
    <ChatDrawerBody
      activeJarvisChatSection={activeJarvisChatSection}
      messages={jarvisChatDrawerFixture.messages}
      projectContextSummary={jarvisChatDrawerFixture.projectContextSummary}
      handoffs={jarvisChatDrawerFixture.handoffs}
      diagnosticsMessages={diagnosticsMessages}
    />
  );

  const overlayShellStyle: React.CSSProperties = {
    position: "relative",
    height: mainVisualHeight,
    borderRadius: 24,
    overflow: "hidden",
    border: "1px solid rgba(255,255,255,0.08)",
    background:
      "radial-gradient(circle at center, rgba(22,36,72,0.32), rgba(6,10,24,0.96))",
  };

  const glassPanelBase: React.CSSProperties = {
    position: "absolute",
    zIndex: 20,
    border: "1px solid rgba(255,255,255,0.08)",
    background: "rgba(10, 16, 34, 0.34)",
    backdropFilter: "blur(16px)",
    boxShadow: "0 20px 60px rgba(0,0,0,0.18)",
    overflow: "auto",
  };

  const lightweightCardStyle: React.CSSProperties = {
    background: "rgba(255,255,255,0.018)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(255,255,255,0.07)",
    boxShadow: "0 10px 28px rgba(0,0,0,0.10)",
  };

  return (
    <div
      className="page-shell"
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <main style={overlayShellStyle}>
        <TopStatusStrip
          title={jarvisChatDrawerContract.collapsedStripLabel}
          isExpanded={drawerShellState.topMode !== "hidden"}
          topStripHeight={topStripHeight}
          backdropBlurPx={jarvisChatDrawerContract.backdropBlurPx}
          onToggle={toggleTopDrawer}
        />

        {operatorZoneAppBinding.showLeftHandle ? (
          <button
            type="button"
            onClick={toggleLeftDrawer}
            style={{
              position: "absolute",
              top: "50%",
              left: 10,
              transform: "translateY(-50%)",
              zIndex: 40,
              writingMode: "vertical-rl",
              textOrientation: "mixed",
              padding: "12px 8px",
              borderRadius: 999,
              border: "1px solid rgba(255,255,255,0.12)",
              background: "rgba(10,16,34,0.32)",
              backdropFilter: `blur(${overlayLayoutContract.drawers.left.backdropBlurPx}px)`,
              color: "white",
              cursor: "pointer",
            }}
          >
            {overlayLayoutContract.drawers.left.handleLabel}
          </button>
        ) : null}

        {operatorZoneAppBinding.showRightHandle ? (
          <button
            type="button"
            onClick={toggleRightDrawer}
            style={{
              position: "absolute",
              top: "50%",
              right: 10,
              transform: "translateY(-50%)",
              zIndex: 40,
              writingMode: "vertical-rl",
              textOrientation: "mixed",
              padding: "12px 8px",
              borderRadius: 999,
              border: "1px solid rgba(255,255,255,0.12)",
              background: "rgba(10,16,34,0.32)",
              backdropFilter: `blur(${overlayLayoutContract.drawers.right.backdropBlurPx}px)`,
              color: "white",
              cursor: "pointer",
            }}
          >
            {overlayLayoutContract.drawers.right.handleLabel}
          </button>
        ) : null}

<TopChatDrawer
  isOpen={operatorZoneAppBinding.showTopCommunicationOverlay}
  topStripHeight={topStripHeight}
  overlayOpacity={jarvisChatDrawerContract.overlayOpacity}
  backdropBlurPx={jarvisChatDrawerContract.backdropBlurPx}
  compactHeaderSpacing={topCommunicationDensityAppBinding.compactHeaderSpacing}
  showSectionTabs={topCommunicationDensityAppBinding.showSectionTabs}
  showSurfaceSelector={topCommunicationDensityAppBinding.showSurfaceSelector}
  collapseSurfaceSelector={
    topCommunicationDensityAppBinding.collapseSurfaceSelector
  }
  showSummaryChipLane={topCommunicationDensityAppBinding.showSummaryChipLane}
  collapseSummaryChipLane={
    topCommunicationDensityAppBinding.collapseSummaryChipLane
  }
  showSupportMeta={topCommunicationDensityAppBinding.showSupportMeta}
  contentDominant={topCommunicationDensityAppBinding.contentDominant}
  topCommunicationDensityMode={topCommunicationDensityAppBinding.mode}
  activeJarvisChatSection={activeJarvisChatSection}
  activeEmbeddedChatSurface={activeEmbeddedChatSurface}
  jarvisChatSections={jarvisChatDrawerContract.sections}
  topDrawerExposureGroup={topDrawerExposureGroup}
  onJarvisChatSectionChange={setActiveJarvisChatSection}
  onEmbeddedChatSurfaceChange={activateEmbeddedChatSurface}
  getJarvisChatSectionTitle={getJarvisChatSectionTitle}
  renderTopDrawerBody={renderTopDrawerBody}
  renderSidebar={() => (
    <ChatSidebar
      activeJarvisChatSection={activeJarvisChatSection}
      activeEmbeddedChatSurfaceLabel={activeEmbeddedChatSurfaceLabel}
      jarvisChatSections={jarvisChatDrawerContract.sections}
      onJarvisChatSectionChange={setActiveJarvisChatSection}
      getJarvisChatSectionTitle={getJarvisChatSectionTitle}
      unreadCount={jarvisChatDrawerReadModel.unreadCount}
      codeBlockCount={jarvisChatDrawerReadModel.codeBlockCount}
      handoffCount={jarvisChatDrawerFixture.handoffs.length}
      diagnosticCount={diagnosticsMessages.length}
    />
  )}
/>

        <SummaryCardsOverlay
          isVisible={operatorZoneAppBinding.showSummaryCards}
          topStripHeight={topStripHeight}
          activeViewTitle={activeEntry.title}
          nodeCountLabel={
            activeGraphViewKey
              ? String(graphProjectionRegistry[activeGraphViewKey].nodes.length)
              : "—"
          }
          unreadCount={jarvisChatDrawerReadModel.unreadCount}
          codeBlockCount={jarvisChatDrawerReadModel.codeBlockCount}
        />

        <section
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 1,
          }}
        >
          {activeGraphViewKey ? (
            <div style={{ position: "absolute", inset: 0 }}>
              <ReactFlow
                key={`graph-flow:${activeGraphViewKey}`}
                nodes={nodes}
                edges={edges}
                fitView
                attributionPosition="bottom-left"
                proOptions={{ hideAttribution: true }}
                nodesDraggable={false}
                nodesConnectable={false}
                elementsSelectable={true}
                panOnDrag={true}
                zoomOnScroll={true}
                zoomOnPinch={true}
                onInit={(instance) => {
                  window.requestAnimationFrame(() => {
                    instance.fitView({ padding: 0.16 });
                  });
                }}
                onNodeClick={(_, node) => {
                  const payload = selectedNodeMap.get(node.id);
                  if (payload) {
                    setSelectedItem({
                      kind: "node",
                      viewKey: activeGraphViewKey,
                      payload,
                    });
                    setDrawerShellState((current) => ({
                      ...current,
                      rightMode: "expanded",
                      activeRightSection: "inspect",
                    }));
                  }
                }}
                onEdgeClick={(_, edge) => {
                  const payload = selectedEdgeMap.get(edge.id);
                  if (payload) {
                    setSelectedItem({
                      kind: "edge",
                      viewKey: activeGraphViewKey,
                      payload,
                    });
                    setDrawerShellState((current) => ({
                      ...current,
                      rightMode: "expanded",
                      activeRightSection: "inspect",
                    }));
                  }
                }}
              >
                <MiniMap />
                <Controls />
                <Background />
              </ReactFlow>
            </div>
          ) : (
            <div
              style={{
                position: "absolute",
                inset: 0,
                paddingTop: topStripHeight + 16,
              }}
            >
              <div ref={chartHostRef} className="chart-host" />
            </div>
          )}
        </section>

        <LeftDashboardDrawer
          isVisible={operatorZoneAppBinding.showLeftDrawer}
          topStripHeight={topStripHeight}
          drawerWidth={overlayLayoutContract.drawers.left.expandedSizePx}
          drawerOpacity={overlayLayoutContract.drawers.left.opacity}
          drawerBackdropBlurPx={
            overlayLayoutContract.drawers.left.backdropBlurPx
          }
          activeLeftSection={drawerShellState.activeLeftSection}
          leftDrawerSections={leftDrawerSections}
          onLeftSectionChange={(section) =>
            setDrawerShellState((current) => ({
              ...current,
              activeLeftSection: section,
            }))
          }
          getLeftSectionTitle={getLeftSectionTitle}
          renderBody={renderLeftDrawerBody}
        />

        {operatorZoneAppBinding.showRightDrawer ? (
          <aside
            style={{
              ...glassPanelBase,
              top: topStripHeight,
              bottom: 16,
              right: 0,
              width: overlayLayoutContract.drawers.right.expandedSizePx,
              opacity: overlayLayoutContract.drawers.right.opacity,
              backdropFilter: `blur(${overlayLayoutContract.drawers.right.backdropBlurPx}px)`,
              padding: "16px 14px 18px 14px",
            }}
          >
            <div className="view-switcher-group-shell">
              <section className="view-switcher-group">
                <div className="view-switcher-group-title">Right Drawer</div>
                <div
                  className="view-switcher"
                  style={{
                    display: "flex",
                    flexWrap: "nowrap",
                    overflowX: "auto",
                    gap: 8,
                  }}
                >
                  {rightDrawerSections.map((section) => (
                    <button
                      key={section}
                      type="button"
                      className={
                        drawerShellState.activeRightSection === section
                          ? "view-switch-button active"
                          : "view-switch-button"
                      }
                      onClick={() =>
                        setDrawerShellState((current) => ({
                          ...current,
                          activeRightSection: section,
                        }))
                      }
                    >
                      {getRightSectionTitle(section)}
                    </button>
                  ))}
                </div>
              </section>
            </div>

            {renderRightDrawerBody()}
          </aside>
        ) : null}
      </main>

      {operatorZoneAppBinding.showFooter ? (
        <footer
          style={{
            borderRadius: 20,
            border: "1px solid rgba(255,255,255,0.08)",
            background: "rgba(10,16,34,0.34)",
            backdropFilter: "blur(14px)",
            boxShadow: "0 14px 36px rgba(0,0,0,0.16)",
            padding: "12px 16px",
            display: "grid",
            gap: 10,
          }}
        >
          <div
            style={{
              display: "flex",
              gap: 10,
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <span
              style={{
                fontSize: 12,
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                opacity: 0.72,
              }}
            >
              System Footer
            </span>

            <span className="inspect-chip">Environment: DEV</span>
            <span className="inspect-chip">Network: Stable</span>
            <span className="inspect-chip">View: {activeEntry.title}</span>
            <span className="inspect-chip">
              Shell Mode: {operatorZoneAppBinding.shellMode}
            </span>
            <span className="inspect-chip">
              Center Immutable:{" "}
              {String(operatorZoneAppBinding.centerImmutableConfirmed)}
            </span>
            <span className="inspect-chip">
              Family Presence: {presenceItems.length} online
            </span>
          </div>

          <div
            style={{
              display: "flex",
              gap: 8,
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <button type="button" className="view-switch-button active">
              Family Surface
            </button>

            <button type="button" className="view-switch-button">
              Presence Board
            </button>

            {presenceItems.map((item) => (
              <button
                key={item}
                type="button"
                className="view-switch-button"
              >
                {item}
              </button>
            ))}
          </div>
        </footer>
      ) : null}
    </div>
  );
}
