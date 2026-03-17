#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/federation"

cat > node_identity.v1.yaml <<'YAML'
contract_name: node_identity
schema_version: node_identity.v1
description: Canonical identity record for one JARVIS node.

required:
  - node_id
  - node_name
  - node_type
  - role
  - deployment_mode

fields:
  node_id:
    type: string
    description: Unique node identifier.

  node_name:
    type: string
    description: Human-readable node name.

  node_type:
    type: string
    enum:
      - server
      - desktop
      - android
      - ios
      - edge
    description: Canonical platform type of the node.

  role:
    type: string
    description: Node role within the federation.

  deployment_mode:
    type: string
    description: Deployment mode assigned to this node.

  capability_profile_ref:
    type: string
    description: Reference to capability profile assigned to the node.

  owner_scope:
    type: string
    description: Ownership or federation scope of the node.

  trust_policy_ref:
    type: string
    description: Reference to trust policy governing this node.

validation_rules:
  - node_id must be unique
  - node_type must match allowed enum
  - role must be explicit
  - deployment_mode must be explicit

security_rules:
  - identity does not imply sync rights
  - node identity does not imply trust by itself
  - identity metadata must not carry hidden authority
YAML

cat > node_registry.v1.yaml <<'YAML'
contract_name: node_registry
schema_version: node_registry.v1
description: Registry of known nodes in a federation.

required:
  - federation_id
  - nodes

fields:
  federation_id:
    type: string
    description: Unique federation identifier.

  nodes:
    type: array
    items:
      type: string
    description: Explicit list of node identifiers in this federation.

  primary_node_ref:
    type: string
    description: Optional reference to the primary node of the federation.

validation_rules:
  - federation_id required
  - nodes may not contain duplicates
  - primary_node_ref should reference one of nodes when present

security_rules:
  - registry access policy required
  - registry membership does not imply full synchronization rights
  - node registry changes must remain auditable
YAML

cat > sync_contract.v1.yaml <<'YAML'
contract_name: sync_contract
schema_version: sync_contract.v1
description: Canonical sync policy between nodes.

required:
  - sync_id
  - source_node
  - target_node
  - allowed_objects

fields:
  sync_id:
    type: string
    description: Unique synchronization contract identifier.

  source_node:
    type: string
    description: Source node identifier.

  target_node:
    type: string
    description: Target node identifier.

  allowed_objects:
    type: array
    items:
      type: string
    description: Object categories allowed to be synchronized.

  forbidden_objects:
    type: array
    items:
      type: string
    description: Object categories explicitly forbidden from synchronization.

  mode:
    type: string
    enum:
      - one_way
      - bidirectional
      - offline_pack
    description: Synchronization direction and transport mode.

  trust_ref:
    type: string
    description: Reference to trust policy governing this sync path.

validation_rules:
  - source_node and target_node required
  - source_node and target_node must not be identical
  - allowed_objects should be explicit even when narrow
  - mode must match allowed enum

security_rules:
  - runtime state sync forbidden
  - sync contract does not imply unrestricted data exchange
  - restricted objects require explicit policy gate
YAML

cat > trust_link.v1.yaml <<'YAML'
contract_name: trust_link
schema_version: trust_link.v1
description: Explicit trust relation between two nodes.

required:
  - trust_link_id
  - source_node
  - target_node
  - trust_level

fields:
  trust_link_id:
    type: string
    description: Unique trust-link identifier.

  source_node:
    type: string
    description: Origin node of trust relation.

  target_node:
    type: string
    description: Target node of trust relation.

  trust_level:
    type: string
    description: Effective trust level between source and target.

  capabilities_granted:
    type: array
    items:
      type: string
    description: Capability categories permitted under this trust link.

validation_rules:
  - source_node and target_node required
  - source_node and target_node must not be identical
  - capabilities_granted should be explicit even when empty

security_rules:
  - trust link cannot override denied categories
  - trust link does not bypass approval policy
  - granted capabilities must remain bounded by governance
YAML

cat > federation_snapshot.v1.yaml <<'YAML'
contract_name: federation_snapshot
schema_version: federation_snapshot.v1
description: Snapshot of node topology and current known statuses.

required:
  - snapshot_id
  - federation_id
  - nodes

fields:
  snapshot_id:
    type: string
    description: Unique federation snapshot identifier.

  federation_id:
    type: string
    description: Federation identifier for this snapshot.

  nodes:
    type: array
    items:
      type: string
    description: Explicit list of nodes visible in this snapshot.

  statuses:
    type: object
    additional_properties: true
    description: Structured node-status mapping captured at snapshot time.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp when the snapshot was created.

validation_rules:
  - nodes required
  - snapshot_id must be unique
  - created_at required
  - statuses should map only to nodes listed in nodes

security_rules:
  - snapshot visibility follows trust policy
  - snapshot is evidence only
  - snapshot must not expose restricted node metadata outside policy
YAML

echo "federation contracts restored successfully"
