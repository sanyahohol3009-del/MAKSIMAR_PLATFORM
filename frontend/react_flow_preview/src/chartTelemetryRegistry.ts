export type ChartViewKey =
  | "node_resources"
  | "export_validation_assets"
  | "security_telemetry"
  | "summary";

export type ChartSeriesPoint = {
  label: string;
  value: number;
};

export type ChartRegistryEntry = {
  viewKey: ChartViewKey;
  title: string;
  subtitle: string;
  chartKind: "bar" | "line";
  series: ChartSeriesPoint[];
};

export const chartTelemetryRegistry: ReadonlyArray<ChartRegistryEntry> = [
  {
    viewKey: "node_resources",
    title: "Node Resources",
    subtitle: "Bootstrap chart preview for resource-oriented telemetry.",
    chartKind: "bar",
    series: [
      { label: "CPU", value: 62 },
      { label: "RAM", value: 71 },
      { label: "GPU", value: 48 },
      { label: "Storage", value: 57 },
    ],
  },
  {
    viewKey: "export_validation_assets",
    title: "Export / Validation / Assets",
    subtitle: "Bootstrap chart preview for export and validation surfaces.",
    chartKind: "bar",
    series: [
      { label: "Exports", value: 12 },
      { label: "Validated", value: 9 },
      { label: "Assets", value: 17 },
    ],
  },
  {
    viewKey: "security_telemetry",
    title: "Security / Telemetry",
    subtitle: "Bootstrap chart preview for security and telemetry signals.",
    chartKind: "line",
    series: [
      { label: "T1", value: 3 },
      { label: "T2", value: 5 },
      { label: "T3", value: 4 },
      { label: "T4", value: 6 },
      { label: "T5", value: 5 },
    ],
  },
  {
    viewKey: "summary",
    title: "Multi-Series Summary",
    subtitle: "Bootstrap summary chart preview for combined visibility.",
    chartKind: "bar",
    series: [
      { label: "Graphs", value: 8 },
      { label: "Charts", value: 4 },
      { label: "Panels", value: 12 },
      { label: "Alerts", value: 3 },
    ],
  },
];

export function getChartRegistryEntry(viewKey: ChartViewKey): ChartRegistryEntry {
  const entry = chartTelemetryRegistry.find((item) => item.viewKey === viewKey);

  if (!entry) {
    throw new Error(`Missing chart registry entry for ${viewKey}.`);
  }

  return entry;
}

export function getChartViewOrder(): ChartViewKey[] {
  return chartTelemetryRegistry.map((entry) => entry.viewKey);
}
