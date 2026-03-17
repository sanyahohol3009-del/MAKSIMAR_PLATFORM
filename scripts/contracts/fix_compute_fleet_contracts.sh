#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/compute_fleet"

cat > compute_node.v1.yaml <<'YAML'
contract_name: compute_node
schema_version: compute_node.v1
description: Canonical compute node descriptor.

required:
  - node_id
  - node_type
  - telemetry_fields

fields:
  node_id:
    type: string
    description: Unique compute node identifier.

  node_type:
    type: string
    enum:
      - gpu
      - asic
      - cpu
      - hybrid
    description: Canonical compute node class.

  telemetry_fields:
    type: array
    items:
      type: string
    description: Explicit telemetry fields emitted by the compute node.

  power_profile_ref:
    type: string
    description: Reference to assigned power profile.

  thermal_profile_ref:
    type: string
    description: Reference to assigned thermal profile.

validation_rules:
  - node_id required
  - node_type must match allowed enum
  - telemetry_fields required
  - power_profile_ref and thermal_profile_ref should be explicit for managed nodes

security_rules:
  - telemetry and control boundary explicit
  - compute node metadata does not imply control authority
  - profile bindings must remain reviewable
YAML

cat > rig_inventory.v1.yaml <<'YAML'
contract_name: rig_inventory
schema_version: rig_inventory.v1
description: Inventory of compute or mining rigs.

required:
  - inventory_id
  - nodes

fields:
  inventory_id:
    type: string
    description: Unique inventory identifier.

  nodes:
    type: array
    items:
      type: string
    description: Explicit list of node references included in the inventory.

  owner_scope:
    type: string
    description: Ownership or tenancy scope of the inventory.

validation_rules:
  - inventory_id required
  - nodes required
  - nodes must not contain duplicates
  - owner_scope should be explicit for shared or federated inventories

security_rules:
  - inventory visibility follows product trust and access policy
  - inventory records do not grant node control rights
  - node membership must remain auditable
YAML

cat > thermal_profile.v1.yaml <<'YAML'
contract_name: thermal_profile
schema_version: thermal_profile.v1
description: Thermal constraints for compute nodes.

required:
  - profile_id
  - limits

fields:
  profile_id:
    type: string
    description: Unique thermal profile identifier.

  limits:
    type: object
    additional_properties: true
    description: Structured thermal limits and operating thresholds.

  fan_policy:
    type: object
    additional_properties: true
    description: Structured fan behavior policy associated with this profile.

validation_rules:
  - profile_id required
  - limits required
  - thermal thresholds should be explicit
  - fan_policy should be explicit when thermal automation is supported

security_rules:
  - unsafe thermal states must trigger alerts
  - thermal profiles do not directly authorize hardware writes
  - threshold changes may require approval depending on governance policy
YAML

cat > power_profile.v1.yaml <<'YAML'
contract_name: power_profile
schema_version: power_profile.v1
description: Power limits and operating envelopes for compute nodes.

required:
  - profile_id
  - limits

fields:
  profile_id:
    type: string
    description: Unique power profile identifier.

  limits:
    type: object
    additional_properties: true
    description: Structured power limits and operating envelopes.

  target_efficiency_mode:
    type: string
    description: Preferred efficiency or performance mode targeted by this profile.

validation_rules:
  - profile_id required
  - limits required
  - target_efficiency_mode should be explicit for managed nodes

security_rules:
  - changes may require approval depending on risk
  - power profiles do not by themselves authorize node mutation
  - limits must remain bounded by governance and safety policy
YAML

cat > fleet_alert.v1.yaml <<'YAML'
contract_name: fleet_alert
schema_version: fleet_alert.v1
description: Canonical alert for compute fleet operations.

required:
  - alert_id
  - node_ref
  - severity
  - message

fields:
  alert_id:
    type: string
    description: Unique fleet alert identifier.

  node_ref:
    type: string
    description: Reference to the affected compute node.

  severity:
    type: string
    enum:
      - info
      - warning
      - critical
    description: Alert severity level.

  message:
    type: string
    description: Human-readable alert message.

  recommended_actions:
    type: array
    items:
      type: string
    description: Suggested approved actions for remediation.

validation_rules:
  - alert_id required
  - node_ref required
  - severity must match allowed enum
  - message required
  - recommended_actions should be explicit even when empty

security_rules:
  - alerts are informational until approved action path is chosen
  - alerts must not conceal critical fleet state
  - recommended actions remain subject to approval and action policy
YAML

echo "compute_fleet contracts restored successfully"
