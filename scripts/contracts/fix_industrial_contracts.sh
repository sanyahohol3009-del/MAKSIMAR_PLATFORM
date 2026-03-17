#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/industrial"

cat > digital_twin.v1.yaml <<'YAML'
contract_name: digital_twin
schema_version: digital_twin.v1
description: Canonical digital twin descriptor.

required:
  - twin_id
  - twin_type
  - source_model_refs

fields:
  twin_id:
    type: string
    description: Unique digital twin identifier.

  twin_type:
    type: string
    description: Canonical type or domain class of the digital twin.

  source_model_refs:
    type: array
    items:
      type: string
    description: References to source models or engineering artifacts used to build the twin.

  telemetry_bindings:
    type: array
    items:
      type: string
    description: Explicit telemetry bindings associated with the digital twin.

validation_rules:
  - twin_id required
  - twin_type required
  - source_model_refs required
  - source_model_refs must not be empty
  - telemetry_bindings should be explicit even when empty

security_rules:
  - digital twin does not directly control plant hardware
  - twin metadata must remain traceable to source artifacts
  - telemetry bindings do not imply write authority
YAML

cat > plc_adapter.v1.yaml <<'YAML'
contract_name: plc_adapter
schema_version: plc_adapter.v1
description: PLC interface contract boundary.

required:
  - adapter_id
  - supported_protocols

fields:
  adapter_id:
    type: string
    description: Unique PLC adapter identifier.

  supported_protocols:
    type: array
    items:
      type: string
    description: Explicit list of supported PLC communication protocols.

  control_mode:
    type: string
    enum:
      - read_only
      - limited_control
      - blocked
    description: Allowed control boundary for this PLC adapter.

validation_rules:
  - adapter_id required
  - supported_protocols required
  - supported_protocols must not be empty
  - control_mode must match allowed enum

security_rules:
  - read_only default
  - control authority must remain policy-gated
  - adapter boundary must not bypass industrial safety constraints
YAML

cat > scada_bridge.v1.yaml <<'YAML'
contract_name: scada_bridge
schema_version: scada_bridge.v1
description: SCADA bridge contract.

required:
  - bridge_id
  - mode

fields:
  bridge_id:
    type: string
    description: Unique SCADA bridge identifier.

  mode:
    type: string
    enum:
      - read_only
      - limited_control
      - blocked
    description: Allowed SCADA bridge operating mode.

  signal_map_ref:
    type: string
    description: Reference to signal mapping configuration or artifact.

validation_rules:
  - bridge_id required
  - mode must match allowed enum
  - signal_map_ref should be explicit for connected bridges

security_rules:
  - write and control remain restricted by policy
  - read_only is the safe baseline
  - bridge metadata does not authorize industrial actuation
YAML

cat > industrial_constraint.v1.yaml <<'YAML'
contract_name: industrial_constraint
schema_version: industrial_constraint.v1
description: Industrial safety constraint model.

required:
  - constraint_id
  - severity
  - rule

fields:
  constraint_id:
    type: string
    description: Unique industrial constraint identifier.

  severity:
    type: string
    enum:
      - warning
      - critical
      - hard_stop
    description: Severity class of the industrial constraint.

  rule:
    type: string
    description: Human-readable or machine-evaluable rule definition.

  applies_to:
    type: string
    description: Target subsystem, twin, adapter, or industrial scope this constraint applies to.

validation_rules:
  - constraint_id required
  - severity must match allowed enum
  - rule required
  - applies_to should be explicit

security_rules:
  - hard_stop constraints are highest priority
  - constraints must not be bypassed by shell, workflow, or adapter layers
  - constraint violations must remain visible and blocking where policy requires
YAML

echo "industrial contracts restored successfully"
