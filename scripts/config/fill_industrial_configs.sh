#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/INDUSTRIAL_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > digital_twin_policy.yaml <<'YAML'
schema_version: industrial_digital_twin_policy.v1
description: Canonical policy for industrial digital twin operation and validation.

twin_policy:
  model_reference_required: true
  telemetry_binding_required: true
  simulation_alignment_required: true
  direct_hardware_control_forbidden: true

validation:
  twin_consistency_check_required: true
  source_model_traceability_required: true
  update_audit_required: true

rules:
  - digital twin is evidence and modeling layer, not plant authority
  - twin updates must preserve provenance
  - digital twin outputs must not bypass industrial approval paths
YAML

cat > plc_scada_policy.yaml <<'YAML'
schema_version: industrial_plc_scada_policy.v1
description: Canonical policy for PLC and SCADA boundary adapters.

defaults:
  plc_read_only_default: true
  scada_read_only_default: true
  limited_control_requires_policy: true
  blocked_mode_supported: true

validation:
  protocol_whitelist_required: true
  signal_map_reference_required: true
  adapter_audit_required: true

rules:
  - PLC and SCADA adapters default to read-only
  - limited control must remain explicit and policy-gated
  - industrial adapters must not bypass safety constraints
YAML

cat > industrial_constraint_policy.yaml <<'YAML'
schema_version: industrial_constraint_policy.v1
description: Canonical policy for industrial safety constraints and blocking rules.

constraints:
  warning_enabled: true
  critical_enabled: true
  hard_stop_enabled: true
  hard_stop_highest_priority: true

validation:
  applies_to_required: true
  rule_definition_required: true
  constraint_visibility_required: true

rules:
  - hard-stop constraints override lower-priority paths
  - constraint violations must remain visible and blocking where defined
  - no workflow, shell, or adapter may silently weaken industrial constraints
YAML

echo "industrial configs filled successfully"
