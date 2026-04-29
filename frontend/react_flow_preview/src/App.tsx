import React, { useEffect, useMemo, useRef, useState } from "react";
import "@xyflow/react/dist/style.css";

import { graphProjectionRegistry } from "./graphProjectionData.js";
import { buildActiveDashboardRouteReadModel } from "./activeDashboardRouteReadModel.js";
import { buildCenterViewportInputContract } from "./centerViewportInputContract.js";
import {
  buildStyledEdges,
  buildStyledNodes,
} from "./graphVisualSemantics.js";
import {
  buildUnifiedVisualInspectPresentation,
  type SelectedGraphInspectItem,
} from "./unifiedVisualInspectSemantics.js";
import {
  type UnifiedVisualViewId,
} from "./unifiedVisualWorkspaceRegistry.js";
import { buildChartOption } from "./chartTelemetrySemantics.js";
import type {
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
import { buildInitialOverlayDrawerShellState } from "./overlayDrawerShellState.js";

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
import { RightSystemContextDrawer } from "./shell/RightSystemContextDrawer.js";
import { CenterDashboardViewport } from "./shell/CenterDashboardViewport.js";
import { AppShell } from "./shell/AppShell.js";
import { PermanentDashboardNavigationRail } from "./permanentDashboardNavigationRailShellComponent.js";
import { getActiveViewForPermanentRailSurfaceId } from "./permanentRailActiveDashboardSelectionBinding.js";
import {
  buildActiveDashboardLeftDrawerReadModel,
  getActiveDashboardLeftDrawerSectionByAlias,
} from "./activeDashboardLeftDrawerBinding.js";
import {
  ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX,
  LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX,
  SUMMARY_CARDS_LEFT_OFFSET_PX,
} from "./appShellPermanentRailLayoutOffsets.js";
import {
  SHELL_OVERLAY_STYLE,
  SHELL_TOP_STRIP_HEIGHT_PX,
} from "./shell/shellLayoutConstants.js";
import { ShellFooter } from "./shell/ShellFooter.js";
import { DrawerHandles } from "./shell/DrawerHandles.js";
import { InspectPresentationView } from "./shell/InspectPresentationView.js";
import { useDrawerShellInteractions } from "./shell/useDrawerShellInteractions.js";

import { ChatConversationPane } from "./features/chat/ChatConversationPane.js";
import { ChatInputBar } from "./features/chat/ChatInputBar.js";
import { ChatSidebar } from "./features/chat/ChatSidebar.js";
import { ChatDrawerBody } from "./features/chat/ChatDrawerBody.js";
import {
  getEmbeddedChatSurfaceLabel,
  getPreferredJarvisSection,
} from "./features/chat/embeddedChatSurfaceHelpers.js";

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

  const {
    toggleLeftDrawer,
    toggleRightDrawer,
    toggleTopDrawer,
    setActiveLeftDrawerSection,
    setActiveRightDrawerSection,
  } = useDrawerShellInteractions(setDrawerShellState);

  const [activeView, setActiveView] =
    useState<UnifiedVisualViewId>("graph:topology");
  const [activeRailSurfaceId, setActiveRailSurfaceId] =
    useState("operator_home");
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

  const activeDashboardRoute =
    buildActiveDashboardRouteReadModel(activeView);
  const centerViewportInput =
    buildCenterViewportInputContract(activeDashboardRoute);

  const handlePermanentRailSurfaceSelect = (surfaceId: string): void => {
    setActiveRailSurfaceId(surfaceId);

    const nextActiveView = getActiveViewForPermanentRailSurfaceId(surfaceId);

    if (nextActiveView) {
      setActiveView(nextActiveView);
    }
  };

  const activeDashboardLeftDrawer =
 buildActiveDashboardLeftDrawerReadModel({
 activeSurfaceId: activeRailSurfaceId,
 activeView,
 });
 const activeEntry = activeDashboardRoute.activeEntry;
  const workspaceSnapshot = activeDashboardRoute.workspaceSnapshot;

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

  const activeGraphViewKey = centerViewportInput.activeGraphViewKey;

  const activeChartViewKey = centerViewportInput.activeChartViewKey;

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

  const topStripHeight = SHELL_TOP_STRIP_HEIGHT_PX;

  const presenceItems = ["home_001", "dev_001", "mobile_001"];

  const activeEmbeddedChatSurfaceLabel = getEmbeddedChatSurfaceLabel(
    topDrawerExposureGroup,
    activeEmbeddedChatSurface,
  );

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

  const activateEmbeddedChatSurface = (surfaceId: EmbeddedChatSurfaceId) => {
    setActiveEmbeddedChatSurface(surfaceId);
    setActiveJarvisChatSection(getPreferredJarvisSection(surfaceId));
  };


  const renderLeftDrawerBody = () => {
 const activeContextSection = getActiveDashboardLeftDrawerSectionByAlias(
 activeDashboardLeftDrawer,
 drawerShellState.activeLeftSection,
 );

 return (
 <div className="workspace-sidebar-groups">
 <section className="workspace-sidebar-group">
 <h3>{activeContextSection.title}</h3>
 <p className="workspace-sidebar-item-meta">
 {activeContextSection.description}
 </p>
 <div className="workspace-sidebar-items">
 {activeContextSection.items.map((item) => (
 <button
 key={item.itemId}
 type="button"
 className={
 item.enabled
 ? "workspace-sidebar-item active"
 : "workspace-sidebar-item"
 }
 disabled={!item.enabled}
 >
 <span className="workspace-sidebar-item-title">
 {item.title}
 </span>
 <span className="workspace-sidebar-item-meta">
 {item.description}: {item.value}
 </span>
 </button>
 ))}
 </div>
 </section>
 </div>
 );
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
            <InspectPresentationView presentation={memoryKnowledgeShell.activeInspect} />
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
            <InspectPresentationView presentation={panelFamilyTaxonomyExposureInspect} />
          </>
        );

      case "inspect":
      default:
        return (
          <>
            <InspectPresentationView presentation={inspectPresentation} />

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

                <InspectPresentationView presentation={embeddedChatShellExposureInspect} />
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

  const overlayShellStyle = SHELL_OVERLAY_STYLE;

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
    <AppShell
      overlayShellStyle={overlayShellStyle}
      topReservedHeight={topStripHeight}
      topStatusStrip={
        <TopStatusStrip
          title={jarvisChatDrawerContract.collapsedStripLabel}
          isExpanded={drawerShellState.topMode !== "hidden"}
          topStripHeight={topStripHeight}
          backdropBlurPx={jarvisChatDrawerContract.backdropBlurPx}
          onToggle={toggleTopDrawer}
        />
      }
      leftHandle={
        <DrawerHandles
          showLeftHandle={operatorZoneAppBinding.showLeftHandle}
          showRightHandle={false}
          leftLabel={overlayLayoutContract.drawers.left.handleLabel}
          rightLabel=""
          leftBackdropBlurPx={
            overlayLayoutContract.drawers.left.backdropBlurPx
          }
          rightBackdropBlurPx={0}
          leftOffsetPx={LEFT_DRAWER_HANDLE_LEFT_OFFSET_PX}
          onToggleLeft={toggleLeftDrawer}
          onToggleRight={() => {}}
        />
      }
      rightHandle={
        <DrawerHandles
          showLeftHandle={false}
          showRightHandle={operatorZoneAppBinding.showRightHandle}
          leftLabel=""
          rightLabel={overlayLayoutContract.drawers.right.handleLabel}
          leftBackdropBlurPx={0}
          rightBackdropBlurPx={
            overlayLayoutContract.drawers.right.backdropBlurPx
          }
          onToggleLeft={() => {}}
          onToggleRight={toggleRightDrawer}
        />
      }
      topChatDrawer={
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
      }
      summaryCardsOverlay={
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
          leftOffsetPx={SUMMARY_CARDS_LEFT_OFFSET_PX}
        />
      }
      permanentRail={
        <PermanentDashboardNavigationRail
            activeSurfaceId={activeRailSurfaceId}
            density="expanded"
            onSelectSurface={handlePermanentRailSurfaceSelect}
          />
      }
      centerViewport={
        <CenterDashboardViewport
          activeGraphViewKey={activeGraphViewKey}
          nodes={nodes}
          edges={edges}
          chartHostRef={chartHostRef}
          selectedNodeMap={selectedNodeMap}
          selectedEdgeMap={selectedEdgeMap}
          onNodeInspect={({ viewKey, payload }) => {
            setSelectedItem({
              kind: "node",
              viewKey,
              payload,
            });
            setDrawerShellState((current) => ({
              ...current,
              rightMode: "expanded",
              activeRightSection: "inspect",
            }));
          }}
          onEdgeInspect={({ viewKey, payload }) => {
            setSelectedItem({
              kind: "edge",
              viewKey,
              payload,
            });
            setDrawerShellState((current) => ({
              ...current,
              rightMode: "expanded",
              activeRightSection: "inspect",
            }));
          }}
        />
      }
      leftDrawer={
        <LeftDashboardDrawer
          isVisible={operatorZoneAppBinding.showLeftDrawer}
          topStripHeight={topStripHeight}
          drawerWidth={overlayLayoutContract.drawers.left.expandedSizePx}
          leftOffsetPx={ACTIVE_DASHBOARD_LEFT_DRAWER_LEFT_OFFSET_PX}
          drawerOpacity={overlayLayoutContract.drawers.left.opacity}
          drawerBackdropBlurPx={
            overlayLayoutContract.drawers.left.backdropBlurPx
          }
          activeLeftSection={drawerShellState.activeLeftSection}
          leftDrawerSections={leftDrawerSections}
          onLeftSectionChange={setActiveLeftDrawerSection}
          getLeftSectionTitle={getLeftSectionTitle}
          renderBody={renderLeftDrawerBody}
        />
      }
      rightDrawer={
        <RightSystemContextDrawer
          isVisible={operatorZoneAppBinding.showRightDrawer}
          topStripHeight={topStripHeight}
          drawerWidth={overlayLayoutContract.drawers.right.expandedSizePx}
          drawerOpacity={overlayLayoutContract.drawers.right.opacity}
          drawerBackdropBlurPx={
            overlayLayoutContract.drawers.right.backdropBlurPx
          }
          activeRightSection={drawerShellState.activeRightSection}
          rightDrawerSections={rightDrawerSections}
          onRightSectionChange={setActiveRightDrawerSection}
          getRightSectionTitle={getRightSectionTitle}
          renderBody={renderRightDrawerBody}
        />
      }
      footer={
        <ShellFooter
          isVisible={operatorZoneAppBinding.showFooter}
          activeViewTitle={activeEntry.title}
          shellMode={operatorZoneAppBinding.shellMode}
          centerImmutableConfirmed={
            operatorZoneAppBinding.centerImmutableConfirmed
          }
          presenceItems={presenceItems}
        />
      }
    />
  );
}
