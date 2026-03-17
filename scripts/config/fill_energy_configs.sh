#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/ENERGY_OPERATIONS_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > solar_policy.yaml <<'YAML'
schema_version: energy_solar_policy.v1
description: Canonical telemetry and control-boundary policy for solar inputs.

telemetry:
  telemetry_required: true
  power_input_tracking_enabled: true
  source_identity_required: true

control:
  direct_control_forbidden_by_default: true
  approval_required_for_control_change: true

rules:
  - solar telemetry does not imply control authority
  - solar source identity must remain explicit
  - control changes remain policy-gated
YAML

cat > battery_policy.yaml <<'YAML'
schema_version: energy_battery_policy.v1
description: Canonical policy for battery monitoring and bounded control flows.

monitoring:
  charge_tracking_required: true
  temperature_tracking_required: true
  health_tracking_required: true

control:
  charging_control_policy_gated: true
  unsafe_state_must_trigger_alert: true
  direct_hardware_override_forbidden: true

rules:
  - unsafe battery state must remain visible
  - monitoring is default, control is gated
  - battery policy must not bypass governance
YAML

cat > inverter_policy.yaml <<'YAML'
schema_version: energy_inverter_policy.v1
description: Canonical inverter telemetry and control-boundary policy.

monitoring:
  state_tracking_required: true
  power_in_tracking_required: true
  power_out_tracking_required: true
  alarms_required: true

control:
  direct_mode_switch_forbidden_by_default: true
  approval_required_for_control_actions: true

rules:
  - inverter alarms must remain visible
  - telemetry must be preserved even when control is blocked
  - inverter policy remains bounded by governance
YAML

cat > load_balancing_policy.yaml <<'YAML'
schema_version: energy_load_balancing_policy.v1
description: Canonical policy for energy-aware balancing decisions and rules.

ruleset:
  trigger_conditions_required: true
  approved_actions_only: true
  priority_required_for_overlapping_rules: true

execution:
  simulation_or_preview_recommended: true
  direct_hardware_execution_forbidden_by_default: true
  approval_required_for_sensitive_actions: true

rules:
  - balancing rules do not bypass action policy
  - sensitive balancing actions remain approval-gated
  - hidden or implicit control paths are forbidden
YAML

cat > energy_schedule_policy.yaml <<'YAML'
schema_version: energy_schedule_policy.v1
description: Canonical schedule policy for energy-aware compute and load planning.

scheduling:
  explicit_time_windows_required: true
  linked_assets_required: true
  policy_review_required_for_critical_assets: true

execution:
  schedule_is_advisory_until_approved: true
  automatic_high_risk_changes_forbidden: true

rules:
  - energy schedules do not imply execution authority
  - critical-asset schedule changes must remain reviewable
  - schedule provenance must remain visible
YAML

echo "energy configs filled successfully"
