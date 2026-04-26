import test from "node:test";
import assert from "node:assert/strict";

import { buildChartOption } from "../react_flow_preview/src/chartTelemetrySemantics.js";

test("bar chart option is built for node resources", () => {
  const option = buildChartOption("node_resources");

  assert.equal(Array.isArray(option.series), true);
  assert.equal(option.xAxis !== undefined, true);
  assert.equal(option.yAxis !== undefined, true);
});

test("line chart option is built for security telemetry", () => {
  const option = buildChartOption("security_telemetry");

  assert.equal(Array.isArray(option.series), true);
  assert.equal(option.tooltip !== undefined, true);
});

test("summary chart option remains buildable", () => {
  const option = buildChartOption("summary");

  assert.equal(option.title !== undefined, true);
});
