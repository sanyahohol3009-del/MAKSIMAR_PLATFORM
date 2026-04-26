import test from "node:test";
import assert from "node:assert/strict";

import {
  chartTelemetryRegistry,
  getChartRegistryEntry,
  getChartViewOrder,
} from "../react_flow_preview/src/chartTelemetryRegistry.js";

test("chart registry exposes stable order", () => {
  assert.deepEqual(getChartViewOrder(), [
    "node_resources",
    "export_validation_assets",
    "security_telemetry",
    "summary",
  ]);
});

test("chart registry contains four entries", () => {
  assert.equal(chartTelemetryRegistry.length, 4);
});

test("chart registry exposes node resources entry", () => {
  const entry = getChartRegistryEntry("node_resources");

  assert.equal(entry.title, "Node Resources");
  assert.equal(entry.chartKind, "bar");
  assert.equal(entry.series.length, 4);
});
