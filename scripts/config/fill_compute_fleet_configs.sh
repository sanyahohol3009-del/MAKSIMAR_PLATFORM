#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/COMPUTE_FLEET_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > fleet_registry.yaml <<'YAML'
schema_version: compute_fleet_registry.v1
description: Canonical registry configuration for compute fleet nodes and inventories.

registry:
  gpu_nodes_enabled: true
  asic_nodes_enabled: true
  cpu_nodes_enabled: true
  hybrid_nodes_enabled: true
  inventory_tracking_enabled: true

defaults:
  explicit_node_registration_required: true
  hidden_nodes_forbidden: true
  audit_enabled: true

rules:
  - every compute node must be explicitly registered
  - hidden fleet nodes are forbidden
  - registry mutations must remain auditable
YAML

cat > thermal_policy.yaml <<'YAML'
schema_version: compute_fleet_thermal_policy.v1
description: Canonical policy for thermal monitoring and protection of compute fleet nodes.

monitoring:
  temperature_tracking_required: true
  thermal_alerts_required: true
  fan_policy_tracking_required: true

protection:
  unsafe_temperature_must_trigger_alert: true
  unsafe_temperature_must_trigger_throttle_recommendation: true
  direct_emergency_control_requires_policy: true

rules:
  - unsafe thermal state must remain visible
  - thermal policy is protective, not unrestricted control authority
  - thermal actions must remain bounded by governance
YAML

cat > power_policy.yaml <<'YAML'
schema_version: compute_fleet_power_policy.v1
description: Canonical policy for power limits and operating envelopes of compute nodes.

monitoring:
  power_tracking_required: true
  efficiency_tracking_required: true
  profile_reference_required: true

control:
  direct_power_profile_change_requires_policy: true
  unsafe_power_states_must_trigger_alert: true
  unrestricted_power_override_forbidden: true

rules:
  - power policy must preserve explicit profile references
  - unsafe power states must remain visible
  - power control changes remain approval-gated
YAML

cat > recovery_policy.yaml <<'YAML'
schema_version: compute_fleet_recovery_policy.v1
description: Canonical recovery policy for compute node faults and degraded fleet states.

recovery:
  automatic_recovery_allowed_for_low_risk_faults: true
  automatic_recovery_for_high_risk_faults: false
  recovery_audit_required: true
  root_cause_capture_required: true

classification:
  low_risk_faults:
    - transient_telemetry_gap
    - recoverable_worker_crash
  high_risk_faults:
    - repeated_overheat
    - repeated_power_fault
    - hardware_instability

rules:
  - high-risk faults must not auto-recover without policy
  - recovery actions must preserve incident visibility
  - recovery does not bypass safety or governance
YAML

cat > alerting_policy.yaml <<'YAML'
schema_version: compute_fleet_alerting_policy.v1
description: Canonical alerting policy for compute fleet monitoring.

alerts:
  info_enabled: true
  warning_enabled: true
  critical_enabled: true
  recommended_actions_included: true

requirements:
  node_reference_required: true
  severity_required: true
  message_required: true

rules:
  - alerts are informational until approved action path is chosen
  - critical alerts must remain visible
  - recommended actions must remain policy-bounded
YAML

echo "compute_fleet configs filled successfully"
