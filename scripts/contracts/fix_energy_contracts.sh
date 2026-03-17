#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/energy"

cat > solar_node.v1.yaml <<'YAML'
contract_name: solar_node
schema_version: solar_node.v1
description: Canonical solar telemetry node.

required:
  - solar_node_id
  - node_name
  - telemetry_fields

fields:
  solar_node_id:
    type: string
    description: Unique solar node identifier.

  node_name:
    type: string
    description: Human-readable solar node name.

  telemetry_fields:
    type: array
    items:
      type: string
    description: Explicit telemetry fields emitted by this solar node.

  update_interval_sec:
    type: integer
    description: Expected telemetry update interval in seconds.

validation_rules:
  - solar_node_id required
  - node_name required
  - telemetry_fields required
  - update_interval_sec should be positive when present

security_rules:
  - telemetry node does not imply control authority
  - source telemetry must remain explicit and auditable
  - solar node metadata must not embed hidden control actions
YAML

cat > battery_state.v1.yaml <<'YAML'
contract_name: battery_state
schema_version: battery_state.v1
description: Canonical battery state record.

required:
  - battery_id
  - charge_percent
  - health_state

fields:
  battery_id:
    type: string
    description: Unique battery state identifier or battery asset identifier.

  charge_percent:
    type: number
    description: Current state of charge in percent.

  health_state:
    type: string
    description: Human-readable or normalized health classification.

  temperature_c:
    type: number
    description: Current battery temperature in Celsius.

  last_updated_at:
    type: string
    format: date-time
    description: UTC timestamp of the latest battery state update.

validation_rules:
  - battery_id required
  - charge_percent must be bounded by policy
  - health_state required
  - last_updated_at should be explicit for persisted telemetry records

security_rules:
  - telemetry only unless separately approved for control
  - battery state records do not imply actuator control rights
  - dangerous state visibility must not be suppressed
YAML

cat > inverter_state.v1.yaml <<'YAML'
contract_name: inverter_state
schema_version: inverter_state.v1
description: Canonical inverter telemetry and control-boundary record.

required:
  - inverter_id
  - state

fields:
  inverter_id:
    type: string
    description: Unique inverter identifier.

  state:
    type: string
    description: Current inverter state classification.

  power_in_w:
    type: number
    description: Current measured input power in watts.

  power_out_w:
    type: number
    description: Current measured output power in watts.

  alarms:
    type: array
    items:
      type: string
    description: Explicit inverter alarms or warnings.

validation_rules:
  - inverter_id required
  - state required
  - alarms should be explicit even when empty
  - power values should be numeric when present

security_rules:
  - alarms preserved
  - inverter telemetry does not imply direct control authority
  - state records must remain reviewable and traceable
YAML

cat > load_balancing_rule.v1.yaml <<'YAML'
contract_name: load_balancing_rule
schema_version: load_balancing_rule.v1
description: Rule for energy-aware balancing.

required:
  - rule_id
  - trigger_conditions
  - actions

fields:
  rule_id:
    type: string
    description: Unique load balancing rule identifier.

  trigger_conditions:
    type: object
    additional_properties: true
    description: Structured trigger conditions for rule activation.

  actions:
    type: array
    items:
      type: string
    description: Approved actions or action references used by the rule.

  priority:
    type: integer
    description: Relative rule priority.

validation_rules:
  - rule_id required
  - trigger_conditions required
  - actions required
  - priority should be explicit for overlapping rules

security_rules:
  - rule execution goes through approval and governance if control is sensitive
  - rules do not bypass action policy
  - rule metadata must not embed hidden privileged execution
YAML

cat > energy_schedule.v1.yaml <<'YAML'
contract_name: energy_schedule
schema_version: energy_schedule.v1
description: Schedule for energy-aware compute and load planning.

required:
  - schedule_id
  - time_windows

fields:
  schedule_id:
    type: string
    description: Unique energy schedule identifier.

  time_windows:
    type: array
    items:
      type: object
    description: Explicit time windows for planned energy behavior.

  linked_assets:
    type: array
    items:
      type: string
    description: Linked assets or nodes participating in the schedule.

validation_rules:
  - schedule_id required
  - time_windows required
  - time_windows must not be empty
  - linked_assets should be explicit even when empty

security_rules:
  - schedule changes may require operator approval
  - schedule definition does not imply execution authority
  - energy schedules must remain bounded by governance and safety policy
YAML

echo "energy contracts restored successfully"
