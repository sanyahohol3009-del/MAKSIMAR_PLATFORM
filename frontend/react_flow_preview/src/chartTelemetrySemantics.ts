import { getChartRegistryEntry, type ChartViewKey } from "./chartTelemetryRegistry.js";

type BasicChartOption = {
  title: {
    text: string;
    subtext: string;
    left: string;
  };
  tooltip: {
    trigger: string;
  };
  xAxis: {
    type: string;
    data: string[];
  };
  yAxis: {
    type: string;
  };
  series: Array<{
    type: string;
    data: number[];
    smooth?: boolean;
  }>;
};

export function buildChartOption(viewKey: ChartViewKey): BasicChartOption {
  const entry = getChartRegistryEntry(viewKey);

  const labels = entry.series.map((point) => point.label);
  const values = entry.series.map((point) => point.value);

  if (entry.chartKind === "line") {
    return {
      title: {
        text: entry.title,
        subtext: entry.subtitle,
        left: "center",
      },
      tooltip: {
        trigger: "axis",
      },
      xAxis: {
        type: "category",
        data: labels,
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          type: "line",
          data: values,
          smooth: false,
        },
      ],
    };
  }

  return {
    title: {
      text: entry.title,
      subtext: entry.subtitle,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: labels,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        type: "bar",
        data: values,
      },
    ],
  };
}
