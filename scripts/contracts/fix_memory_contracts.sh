#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/memory"

cat > memory_entity.v1.yaml <<'YAML'
contract_name: memory_entity
schema_version: memory_entity.v1
description: Canonical entity object for Persistent Personal AI Memory Graph.

required:
  - entity_id
  - entity_type
  - name
  - created_at
  - status
  - source

fields:
  entity_id:
    type: string
    description: Unique stable entity identifier.

  entity_type:
    type: string
    enum:
      - User
      - Project
      - Task
      - Workflow
      - Trigger
      - Device
      - Module
      - Document
      - Session
      - Preference
      - Permission
      - Incident
      - Goal
      - Mode
    description: Canonical memory entity type.

  name:
    type: string
    description: Human-readable primary entity name.

  summary:
    type: string
    description: Short semantic summary of the entity.

  labels:
    type: array
    items:
      type: string
    description: Freeform semantic tags.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp of entity creation.

  updated_at:
    type: string
    format: date-time
    description: UTC timestamp of latest update.

  status:
    type: string
    enum:
      - active
      - inactive
      - archived
      - draft
      - deleted
    description: Entity lifecycle status.

  confidence:
    type: number
    minimum: 0.0
    maximum: 1.0
    description: Confidence in correctness of the entity.

  source:
    type: string
    enum:
      - confirmed_user_context
      - system_observed
      - workflow_generated
      - imported
      - inferred
      - operator_confirmed
    description: Source category of entity creation.

  memory_level:
    type: string
    enum:
      - L0_ephemeral
      - L1_operational
      - L2_project
      - L3_stable_personal
      - L4_restricted
    description: Memory sensitivity and retention tier.

  metadata:
    type: object
    additional_properties: true
    description: Structured domain-specific metadata.

validation_rules:
  - entity_id must be globally unique within graph
  - entity_type must be one of the allowed enum values
  - if source=inferred then confidence must be present
  - L4_restricted entities must be marked explicitly
  - updated_at should not be earlier than created_at when both exist

security_rules:
  - entity does not grant execution authority
  - restricted entities require policy-gated access
  - entity metadata must not embed hidden privileged commands
YAML

cat > memory_relation.v1.yaml <<'YAML'
contract_name: memory_relation
schema_version: memory_relation.v1
description: Canonical typed relation between two memory entities.

required:
  - relation_id
  - from_entity_id
  - relation_type
  - to_entity_id
  - created_at
  - source
  - status

fields:
  relation_id:
    type: string
    description: Unique stable relation identifier.

  from_entity_id:
    type: string
    description: Source entity identifier.

  relation_type:
    type: string
    enum:
      - owns
      - has_task
      - depends_on
      - belongs_to
      - activates
      - runs_on
      - continues
      - affects
      - prefers
      - gates
      - applies_to
      - related_to
      - references
      - part_of
    description: Typed relation connecting two entities.

  to_entity_id:
    type: string
    description: Target entity identifier.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp of relation creation.

  updated_at:
    type: string
    format: date-time
    description: UTC timestamp of latest relation update.

  source:
    type: string
    enum:
      - confirmed_user_context
      - system_observed
      - workflow_generated
      - imported
      - inferred
      - operator_confirmed
    description: Source category for the relation.

  confidence:
    type: number
    minimum: 0.0
    maximum: 1.0
    description: Confidence in correctness of the relation.

  status:
    type: string
    enum:
      - active
      - inactive
      - archived
      - deleted
    description: Relation lifecycle state.

  metadata:
    type: object
    additional_properties: true
    description: Structured relation metadata.

validation_rules:
  - relation_id must be unique
  - from_entity_id must exist
  - to_entity_id must exist
  - if source=inferred then confidence should be present
  - updated_at should not be earlier than created_at when both exist

security_rules:
  - relation does not imply execution authority
  - restricted relations require policy-gated access
  - relations may affect ranking and context only, not direct privileged execution
YAML

cat > memory_event.v1.yaml <<'YAML'
contract_name: memory_event
schema_version: memory_event.v1
description: Canonical episodic event for memory timeline and recency-based reasoning.

required:
  - event_id
  - event_type
  - timestamp
  - source
  - importance

fields:
  event_id:
    type: string
    description: Unique event identifier.

  event_type:
    type: string
    enum:
      - workflow_executed
      - workflow_created
      - workflow_suggested
      - project_phase_updated
      - incident_detected
      - task_completed
      - task_created
      - preference_confirmed
      - suggestion_accepted
      - suggestion_rejected
      - session_started
      - session_closed
      - device_used
      - module_changed
    description: Canonical episodic event type.

  session_id:
    type: string
    description: Optional associated session identifier.

  timestamp:
    type: string
    format: date-time
    description: UTC timestamp of event creation.

  related_entities:
    type: array
    items:
      type: string
    description: Entity identifiers associated with this event.

  summary:
    type: string
    description: Short human-readable event summary.

  details:
    type: object
    additional_properties: true
    description: Structured event payload details.

  importance:
    type: string
    enum:
      - low
      - medium
      - high
      - critical
    description: Event importance level.

  source:
    type: string
    enum:
      - system_observed
      - workflow_generated
      - operator_confirmed
      - imported
      - inferred
    description: Source category of event creation.

  memory_level:
    type: string
    enum:
      - L0_ephemeral
      - L1_operational
      - L2_project
      - L3_stable_personal
      - L4_restricted
    description: Memory level assigned to the event.

validation_rules:
  - event_id must be unique
  - related_entities should reference existing entities where applicable
  - critical events should include summary
  - timestamp is mandatory for ordering

security_rules:
  - event log is append-oriented
  - restricted events require gated access
  - event records do not imply execution authority
YAML

cat > memory_query.v1.yaml <<'YAML'
contract_name: memory_query
schema_version: memory_query.v1
description: Query contract for retrieving structured context from memory graph.

required:
  - query_id
  - query_type
  - issued_at
  - requester
  - target_scope

fields:
  query_id:
    type: string
    description: Unique memory query identifier.

  query_type:
    type: string
    enum:
      - entity_lookup
      - relation_expansion
      - project_context
      - workflow_context
      - session_context
      - preference_lookup
      - recent_events
      - incident_context
      - active_context
      - optimization_candidates
    description: Type of memory query requested.

  issued_at:
    type: string
    format: date-time
    description: UTC timestamp of query creation.

  requester:
    type: string
    enum:
      - DIALOGUE_MANAGER
      - WORKFLOW_ENGINE
      - CONTROL_PLANE
      - AI_ROUTER
      - OPERATOR
      - MONITORING
    description: Requesting subsystem.

  target_scope:
    type: object
    properties:
      entity_ids:
        type: array
        items:
          type: string
      project_id:
        type: string
      workflow_id:
        type: string
      session_id:
        type: string
      device_id:
        type: string
      tags:
        type: array
        items:
          type: string
    description: Explicit target scope for the memory query.

  ranking_policy:
    type: object
    properties:
      use_recency:
        type: boolean
      use_frequency:
        type: boolean
      use_project_relevance:
        type: boolean
      use_confirmation_weight:
        type: boolean
      max_results:
        type: integer
        minimum: 1
    description: Ranking and result-limiting settings.

  access_context:
    type: object
    properties:
      mode:
        type: string
      permission_level:
        type: string
      restricted_access_allowed:
        type: boolean
    description: Access context used for policy evaluation.

validation_rules:
  - query_id must be unique per query request
  - requester must be specified
  - target_scope must not be empty
  - max_results must be positive when present

security_rules:
  - query result must respect access policy
  - restricted memory must not be returned without permission
  - query contract does not imply write or mutation rights
YAML

cat > memory_snapshot.v1.yaml <<'YAML'
contract_name: memory_snapshot
schema_version: memory_snapshot.v1
description: Compact structured snapshot produced from graph memory for fast contextual reasoning.

required:
  - snapshot_id
  - snapshot_type
  - created_at
  - source_query_id
  - entities
  - relations
  - summary

fields:
  snapshot_id:
    type: string
    description: Unique memory snapshot identifier.

  snapshot_type:
    type: string
    enum:
      - active_project_context
      - workflow_context
      - session_context
      - user_context
      - device_context
      - incident_context
      - optimization_context
    description: Canonical snapshot category.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp of snapshot creation.

  source_query_id:
    type: string
    description: Query identifier that produced this snapshot.

  entities:
    type: array
    items:
      type: string
    description: Included entity identifiers.

  relations:
    type: array
    items:
      type: string
    description: Included relation identifiers.

  recent_events:
    type: array
    items:
      type: string
    description: Included recent event identifiers.

  summary:
    type: object
    properties:
      primary_focus:
        type: string
      active_project:
        type: string
      active_task:
        type: string
      active_workflow:
        type: string
      key_preferences:
        type: array
        items:
          type: string
      unresolved_items:
        type: array
        items:
          type: string
    description: Compact structured summary of snapshot context.

  confidence:
    type: number
    minimum: 0.0
    maximum: 1.0
    description: Confidence score for snapshot relevance/completeness.

validation_rules:
  - snapshot_id must be unique
  - source_query_id must reference an existing query
  - summary.primary_focus should be present for active contexts
  - entities and relations should be explicitly listed even if empty arrays are used

security_rules:
  - snapshot inherits access restrictions from underlying entities and relations
  - no privileged authority is implied by snapshot contents
  - restricted items must remain filtered unless policy permits access
YAML

cat > memory_retention.v1.yaml <<'YAML'
contract_name: memory_retention
schema_version: memory_retention.v1
description: Retention and pruning policy for memory levels.

required:
  - levels

fields:
  levels:
    type: object
    additional_properties: true
    description: Retention policy map for all active memory levels.

  pruning_rules:
    type: object
    additional_properties: true
    description: Explicit pruning and archival rules.

validation_rules:
  - all active memory levels must be covered
  - pruning rules should be explicit for inferred or low-confidence records

security_rules:
  - restricted memory pruning must be policy-gated
  - retention policy does not override legal or compliance holds
  - deletion actions require approved path where policy demands
YAML

cat > memory_access.v1.yaml <<'YAML'
contract_name: memory_access
schema_version: memory_access.v1
description: Access policy for querying and mutating memory graph.

required:
  - requester
  - target_level
  - operation

fields:
  requester:
    type: string
    description: Requesting subsystem or operator role.

  target_level:
    type: string
    description: Memory level targeted by this access decision.

  operation:
    type: string
    enum:
      - read
      - write
      - link
      - prune
      - export
    description: Requested memory operation.

  allowed:
    type: boolean
    description: Whether the operation is allowed.

  reason:
    type: string
    description: Structured or human-readable reason for the decision.

validation_rules:
  - requester and operation must be explicit
  - operation must match allowed enum
  - target_level must be present

security_rules:
  - L4 restricted access requires explicit permission context
  - denied access must remain denied unless separately re-evaluated
  - access decision does not override immutable governance
YAML

echo "memory contracts restored successfully"
