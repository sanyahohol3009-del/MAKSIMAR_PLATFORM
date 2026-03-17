#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/MEMORY_SYSTEM/config"
mkdir -p "$BASE"
cd "$BASE"

cat > memory_system.yaml <<'YAML'
schema_version: memory_system_config.v1
description: Canonical top-level configuration for persistent memory system.

storage_policy:
  graph_store_enabled: true
  episodic_store_enabled: true
  workflow_memory_enabled: true
  preference_memory_enabled: true
  permission_memory_enabled: true

snapshot_policy:
  enable_snapshots: true
  max_snapshot_entities: 100
  max_snapshot_relations: 200
  max_recent_events: 50

query_policy:
  default_max_results: 25
  enable_recency_ranking: true
  enable_frequency_ranking: true
  enable_project_relevance: true
  enable_confirmation_weight: true

audit_policy:
  audit_entity_changes: true
  audit_relation_changes: true
  audit_event_ingest: true
  audit_pruning_actions: true

security_policy:
  restricted_memory_enabled: true
  direct_core_write_forbidden: true
  execution_authority_forbidden: true
  restricted_export_requires_policy: true

rules:
  - memory provides context and continuity, not authority
  - memory system must not mutate CORE_ROOT
  - restricted memory requires policy-gated access
  - memory-derived suggestions do not imply automatic execution
YAML

cat > memory_levels.yaml <<'YAML'
schema_version: memory_levels.v1
description: Canonical memory level definitions for retention and access control.

levels:
  L0_ephemeral:
    description: Current-session or extremely short-lived contextual memory.
    retention: session_bound
    restricted: false

  L1_operational:
    description: Recent workflows, actions, execution context, and short-term continuity.
    retention: short_term
    restricted: false

  L2_project:
    description: Project phases, tasks, decisions, milestones, and long-running work context.
    retention: medium_term
    restricted: false

  L3_stable_personal:
    description: Durable user preferences and persistent personal context approved for long-term use.
    retention: long_term
    restricted: false

  L4_restricted:
    description: Sensitive memory requiring explicit policy and permission context.
    retention: policy_bound
    restricted: true

rules:
  - every persisted memory object must map to one level
  - restricted level must never be treated as default-readable
  - level assignment affects both retention and access evaluation
YAML

cat > retention_policy.yaml <<'YAML'
schema_version: retention_policy.v1
description: Retention and archival policy for all memory levels.

retention:
  L0_ephemeral:
    ttl_days: 1
    archive_before_delete: false

  L1_operational:
    ttl_days: 30
    archive_before_delete: true

  L2_project:
    ttl_days: 3650
    archive_before_delete: true

  L3_stable_personal:
    ttl_days: 3650
    archive_before_delete: true

  L4_restricted:
    ttl_days: policy_managed
    archive_before_delete: policy_managed

pruning:
  remove_low_confidence_inferred_relations_after_days: 30
  archive_inactive_sessions_after_days: 14
  archive_old_execution_patterns_after_days: 90
  remove_unlinked_ephemeral_objects_after_days: 7

rules:
  - active memory levels must all have retention policy
  - restricted memory retention is policy-managed only
  - pruning must remain auditable
YAML

cat > access_policy.yaml <<'YAML'
schema_version: memory_access_policy.v1
description: Access policy for reading, writing, linking, pruning, and exporting memory.

access_rules:
  unrestricted_query_levels:
    - L0_ephemeral
    - L1_operational
    - L2_project
    - L3_stable_personal

  restricted_query_levels:
    - L4_restricted

  restricted_access_requires:
    - policy_check
    - permission_context
    - explicit_request_scope

write_rules:
  entity_write_allowed: true
  relation_write_allowed: true
  event_write_allowed: true
  restricted_write_requires_policy: true

export_rules:
  unrestricted_export_allowed: true
  restricted_export_requires_policy: true

forbidden:
  - write_to_CORE_ROOT
  - mutate_security_state
  - privileged_execution
  - unrestricted_export_of_L4_restricted

rules:
  - L4 restricted memory must not be returned without explicit permission context
  - export policy must preserve memory level boundaries
  - access decisions must be explainable and auditable
YAML

cat > ranking_policy.yaml <<'YAML'
schema_version: memory_ranking_policy.v1
description: Ranking policy for memory retrieval and context assembly.

signals:
  recency:
    enabled: true
    weight: 0.30

  frequency:
    enabled: true
    weight: 0.15

  project_relevance:
    enabled: true
    weight: 0.25

  confirmation_weight:
    enabled: true
    weight: 0.20

  task_proximity:
    enabled: true
    weight: 0.10

rules:
  - ranking weights should sum conceptually to full retrieval influence
  - restricted memory must not outrank access policy
  - ranking is advisory and cannot override filtering
YAML

cat > forgetting_policy.yaml <<'YAML'
schema_version: memory_forgetting_policy.v1
description: Canonical forgetting and cleanup policy for weak, stale, and noisy memory.

forgetting_rules:
  remove_unconfirmed_noise: true
  remove_stale_low_value_ephemeral: true
  prune_weak_inferred_relations: true
  preserve_confirmed_project_memory: true
  preserve_stable_personal_memory: true

thresholds:
  weak_relation_confidence_below: 0.40
  low_value_event_importance:
    - low
  stale_ephemeral_days: 7
  stale_inferred_relation_days: 30

rules:
  - forgetting must never silently delete restricted memory outside policy
  - confirmed project and stable personal memory require stronger retention bias
  - destructive forgetting actions must be auditable
YAML

cat > audit_policy.yaml <<'YAML'
schema_version: memory_audit_policy.v1
description: Audit requirements for memory mutations and policy-relevant operations.

audit_events:
  entity_created: true
  entity_updated: true
  relation_created: true
  relation_updated: true
  event_ingested: true
  snapshot_exported: true
  prune_executed: true
  restricted_access_attempted: true

requirements:
  include_actor: true
  include_timestamp: true
  include_target_ref: true
  include_reason: true
  include_policy_ref_when_applicable: true

rules:
  - restricted access attempts must always be logged
  - destructive pruning actions must always be logged
  - audit trail is append-oriented
YAML

echo "memory configs filled successfully"
