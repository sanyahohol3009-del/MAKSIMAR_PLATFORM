import React, { useEffect, useMemo, useRef, useState } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

import {
  getChartRegistryEntry,
  getChartViewOrder,
  type ChartViewKey,
} from "./chartTelemetryRegistry.js";
import { buildChartOption } from "./chartTelemetrySemantics.js";

function ChartPreviewApp() {
  const [activeView, setActiveView] = useState<ChartViewKey>("node_resources");
  const chartHostRef = useRef<HTMLDivElement | null>(null);

  const entry = getChartRegistryEntry(activeView);
  const orderedViews = getChartViewOrder();
  const option = useMemo(() => buildChartOption(activeView), [activeView]);

  useEffect(() => {
    const domNode = chartHostRef.current;
    if (!domNode) {
      return;
    }

    let disposed = false;
    let cleanupFn: (() => void) | null = null;

    const setupChart = async () => {
      const echarts = await import("echarts");

      if (disposed || !chartHostRef.current) {
        return;
      }

      const instance = echarts.init(chartHostRef.current);
      instance.setOption(option);

      const onResize = () => {
        instance.resize();
      };

      window.addEventListener("resize", onResize);

      cleanupFn = () => {
        window.removeEventListener("resize", onResize);
        instance.dispose();
      };

      if (disposed) {
        cleanupFn();
        cleanupFn = null;
      }
    };

    void setupChart();

    return () => {
      disposed = true;
      cleanupFn?.();
      cleanupFn = null;
    };
  }, [option]);

  return (
    <div className="page-shell">
      <header className="page-header">
        <div className="title-block">
          <h1>MAKSIMAR Chart Telemetry Preview</h1>
          <p>{entry.subtitle}</p>
        </div>

        <div className="view-switcher">
          {orderedViews.map((viewKey) => (
            <button
              key={viewKey}
              type="button"
              className={
                viewKey === activeView
                  ? "view-switch-button active"
                  : "view-switch-button"
              }
              onClick={() => setActiveView(viewKey)}
            >
              {getChartRegistryEntry(viewKey).title}
            </button>
          ))}
        </div>
      </header>

      <section className="summary-strip">
        <div className="summary-card">
          <span className="summary-label">Active Chart</span>
          <span className="summary-value">{entry.title}</span>
        </div>
        <div className="summary-card">
          <span className="summary-label">Chart Kind</span>
          <span className="summary-value">{entry.chartKind}</span>
        </div>
        <div className="summary-card">
          <span className="summary-label">Series Points</span>
          <span className="summary-value">{entry.series.length}</span>
        </div>
      </section>

      <main className="workspace-shell-chart">
        <aside className="workspace-sidebar">
          <div className="workspace-sidebar-header">
            <h2>Chart Workspace</h2>
            <p>Temporary ECharts backend for telemetry and status layers.</p>
          </div>

          <div className="workspace-sidebar-groups">
            {orderedViews.map((viewKey) => {
              const item = getChartRegistryEntry(viewKey);
              return (
                <button
                  key={viewKey}
                  type="button"
                  className={
                    viewKey === activeView
                      ? "workspace-sidebar-item active"
                      : "workspace-sidebar-item"
                  }
                  onClick={() => setActiveView(viewKey)}
                >
                  <span className="workspace-sidebar-item-title">{item.title}</span>
                  <span className="workspace-sidebar-item-meta">
                    {item.chartKind} · {item.series.length} points
                  </span>
                </button>
              );
            })}
          </div>
        </aside>

        <section className="chart-stage">
          <div ref={chartHostRef} className="chart-host" />
        </section>

        <aside className="inspect-panel">
          <div className="inspect-header">
            <span className="inspect-kicker">Chart Inspect</span>
            <h2>{entry.title}</h2>
            <p>{entry.subtitle}</p>
          </div>

          <div className="inspect-content">
            <div className="inspect-meta-row">
              <span className="inspect-chip">{entry.viewKey}</span>
              <span className="inspect-chip">{entry.chartKind}</span>
            </div>

            <div className="inspect-explanation">
              <h3>Series Data</h3>
              <p>
                This bootstrap chart preview confirms the chart backend, runtime mount,
                and chart registry path.
              </p>
            </div>

            <div className="inspect-sections">
              <section className="inspect-section">
                <h3>Series Points</h3>
                <div className="inspect-fields">
                  {entry.series.map((point) => (
                    <div
                      key={`${point.label}:${point.value}`}
                      className="inspect-field"
                    >
                      <span className="inspect-field-key">{point.label}</span>
                      <span className="inspect-field-value">{point.value}</span>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </div>
        </aside>
      </main>
    </div>
  );
}

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element #root is missing.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ChartPreviewApp />
  </React.StrictMode>,
);
