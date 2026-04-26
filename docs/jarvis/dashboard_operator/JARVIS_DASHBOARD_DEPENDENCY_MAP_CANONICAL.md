# JARVIS DASHBOARD DEPENDENCY MAP CANONICAL

## Purpose
This document gives JARVIS a compact dependency map for the dashboard/operator domain.

It is not prose-heavy documentation.
It is a dependency and boundary reference.

---

## Core Operator Dependency Spine

operator_intent_contract
-> operator_control_plane_handoff_contract
-> operator_audit_visibility_contract
-> operator_interaction_read_model_contract
-> main_operator_interaction_surface_contract
-> action_queue_panel_content_contract
-> approval_queue_panel_content_contract
-> audit_timeline_panel_content_contract

---

## Meaning of the Spine

### operator_intent_contract
Defines operator intent categories:
- view_request
- navigation_request
- control_request

Also defines:
- approval_required
- trace_id

### operator_control_plane_handoff_contract
Defines:
- control-plane operator gateway
- guarded submission only
- no direct execution
- approval_required
- policy_gate_required

### operator_audit_visibility_contract
Defines:
- audit_timeline_surface
- always_visible_audit_path
- no hidden audit mode
- policy visibility
- approval visibility

### operator_interaction_read_model_contract
Derived operator-visible truth:
- interaction_lane
- interaction_surface_state
- approval_state
- handoff_state
- audit_visibility_state
- approval_required
- handoff_ready
- trace_id
- operator_visible

### main_operator_interaction_surface_contract
Materialized operator interaction surface:
- read_only_surface
- approval_bound_surface
- action_visible
- disabled_state_visible
- forbidden_state_visible
- pending_approval_visible
- audit_visible
- handoff_ready

### action_queue_panel_content_contract
Panel content derived from interaction surface:
- read_only_action_entry
- approval_bound_action_entry
- handoff_ready
- trace_id

### approval_queue_panel_content_contract
Filtered approval-bound content:
- pending_approval_entry
- control_request only
- pending_approval_visible
- approval_required
- handoff_ready

### audit_timeline_panel_content_contract
Canonical operator action audit content:
- operator_action_audit_entry
- audit_visible
- approval_required
- trace_id

---

## Panel Binding / View / Display Dependencies

panel_ids
-> panel_metadata_contract
-> panel_source_binding_contract
-> panel_content_contract
-> panel_binding_contract
-> view_targeting_contract
-> panel_view_display_chain_contract
-> display_runtime_resolver_integration_contract
-> workspace_registry_contract
-> layout_composition_contract
-> workspace_read_model_contract

Meaning:
panel identity, source, content, binding, view, display, workspace, and layout are separate layers.

---

## Restore / Display / Continuity Cluster

display_assignment_registry_contract
-> display_occupancy_contract
-> display_replacement_policy_contract
-> display_conflict_resolution_contract
-> free_display_selection_contract
-> display_placement_routing_contract
-> display_assignment_restore_contract
-> display_restore_continuity_contract
-> display_resolver_decision_contract
-> display_continuity_snapshot_contract
-> display_visual_projection_contract
-> workspace_restore_contract

Meaning:
display and restore semantics are layered and must not be bypassed.

---

## Boundary Rules

### Read-only boundary
The following are read-only truth or read-only derivation layers:
- workspace_read_model_contract
- operator_interaction_read_model_contract
- main_operator_interaction_surface_contract
- queue/audit panel content contracts
- continuity/projection/read-model style contracts

### Governance boundary
The following must remain governance-bearing:
- operator_control_plane_handoff_contract
- operator_audit_visibility_contract
- approval semantics in operator_intent_contract
- guard semantics in operator_interaction_guard_contract

### UI boundary
The following are UI/downstream expression layers:
- panel content contracts
- previews
- panel/view/display bindings
- dashboard surfaces

UI may expose.
UI may not execute.

---

## Safe Extension Entry Points
JARVIS may attach new functionality at these points:
- new panel content contract
- new queue panel
- new audit-like panel
- new dashboard view
- new interaction surface
- new module dashboard surface
- new mobile/voice/gesture dashboard bridge
- new preview surface

JARVIS must not attach uncontrolled logic above the governance spine.

---

## Unsafe Mutation Points
JARVIS must not mutate casually:
- operator_intent core semantics
- control-plane handoff semantics
- audit visibility semantics
- stable panel ids
- canonical display truth
- immutable truth layers
- stop-gate/guard authority

---

## Minimal Dependency Reading Rule for JARVIS
Before changing a dashboard/operator feature, JARVIS must identify:

1. upstream truth contract
2. downstream panel/view/display contract
3. whether approval applies
4. whether audit visibility applies
5. whether the change is read-only or control-like
6. whether preview and domain tests exist

If this map is incomplete, the change is not ready.
