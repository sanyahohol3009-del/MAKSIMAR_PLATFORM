# JARVIS PHASE 06 — OPERATOR INTERACTIVITY CANONICAL

## Status
This document fixes the canonical state of the PHASE 06 operator-interactivity layer for JARVIS.

Current confirmed status:
- PHASE 6.1 — Control Plane Handoff: closed
- PHASE 6.2 — Audit Visibility: closed
- PHASE 6.3 — Interaction Read Model: closed
- PHASE 6.4.1 — Main Operator Interaction Surface: closed
- PHASE 6.5.1 — Action / Approval / Audit Panels: closed

This document is for JARVIS internal platform understanding and future controlled extension.

---

## Purpose of PHASE 06
PHASE 06 formalizes the operator-interaction path for the dashboard layer.

This layer exists to make the following visible and structured:
- what the operator can see
- what remains read-only
- what requires approval
- what may be handed off downstream
- what remains visible through the audit path
- what forbidden or disabled states must remain visible

PHASE 06 does not execute actions.
PHASE 06 does not replace the control plane.
PHASE 06 does not bypass policy, approval, or audit.

---

## Canonical Source-of-Truth Contracts

### 1. operator_control_plane_handoff_contract
Purpose:
- formalizes the operator handoff into the control plane
- permits guarded submission only
- forbids direct execution
- preserves approval_required and policy_gate_required semantics

Meaning:
UI/operator layer may submit, but may not execute.

### 2. operator_audit_visibility_contract
Purpose:
- guarantees that submitted operator actions remain visible through the audit path
- forbids hidden audit mode
- keeps policy visibility and approval visibility visible

Meaning:
audit is not optional and not cosmetic.

### 3. operator_interaction_read_model_contract
Purpose:
- builds the operator-visible interaction read model from:
  - operator intent truth
  - control-plane handoff truth
  - audit visibility truth
- preserves:
  - read_only_lane
  - approval_bound_lane
  - approval_required
  - handoff_ready
  - operator_visible
  - trace_id

Meaning:
this is the canonical operator interaction truth for the dashboard layer.

### 4. main_operator_interaction_surface_contract
Purpose:
- materializes the operator-visible interaction surface
- distinguishes:
  - read_only_surface
  - approval_bound_surface
- makes visible:
  - action_visible
  - disabled_state_visible
  - forbidden_state_visible
  - pending_approval_visible
  - audit_visible
  - handoff_ready

Meaning:
this is the canonical operator interaction surface for the main operator dashboard.

### 5. action_queue_panel_content_contract
Purpose:
- exposes operator actions visible through the action queue panel
- preserves read-only versus approval-bound action semantics
- keeps handoff visibility explicit

### 6. approval_queue_panel_content_contract
Purpose:
- exposes only control requests that require approval
- preserves pending approval visibility
- limits approval queue semantics to approval-bound operator work

### 7. audit_timeline_panel_content_contract
Purpose:
- exposes canonical operator action audit entries
- keeps audit visibility explicit
- preserves approval-required state where applicable

---

## Canonical Operator Interaction Semantics

### Read-only interaction
Applies to:
- view_request
- navigation_request

Rules:
- approval_required = false
- surface_class = read_only_surface
- pending_approval_visible = false
- still operator-visible
- still traceable
- still audit-visible

### Approval-bound interaction
Applies to:
- control_request

Rules:
- approval_required = true
- surface_class = approval_bound_surface
- pending_approval_visible = true
- still handoff-ready
- still audit-visible
- still forbidden-state-visible

### Audit rule
Every operator action entering this layer must remain visible through the audit path.

### Handoff rule
This layer may expose handoff-ready state.
This layer may not execute directly.

---

## Canonical Operator Panels in This Phase

### action_queue
Meaning:
- what the operator is attempting to route or submit
- read-only requests and approval-bound requests remain distinguishable

### approval_queue
Meaning:
- what is pending approval
- only approval-bound control requests belong here

### audit_timeline
Meaning:
- what entered the operator action path and must remain visible
- no hidden audit mode

---

## Invariants That Must Not Be Broken

1. UI does not execute.
2. Interaction surface does not bypass control plane.
3. Approval-bound work must remain approval-bound.
4. Audit visibility must not be removed.
5. Forbidden or disabled state must not be hidden.
6. Traceability must remain present.
7. Canonical dashboard id normalization must remain stable.
8. Operator-visible truth must remain derived from canonical contracts, not ad-hoc UI state.

---

## Forbidden Changes
The following are forbidden:
- direct execution from dashboard interaction surfaces
- hidden audit mode
- skipping approval for control_request
- collapsing read_only and approval_bound semantics into one state
- removing forbidden_state_visible
- removing trace_id visibility semantics
- moving source of truth from contracts into UI-local state
- introducing a second operator truth path outside canonical contracts

---

## Safe Future Extension Zones
Future extension is allowed in:
- new operator panels
- new queue-style views
- new audit surfaces
- new preview layers
- new module/operator bindings
- voice/gesture entry points
- mobile/operator companion surfaces

But all extension must remain downstream of:
- canonical contracts
- control plane handoff
- approval path
- audit visibility
- domain tests
- preview discipline

---

## Canonical Development Rule for This Phase
Any extension of the operator-interactivity layer must follow:

contract
-> models/read-model
-> contract builder
-> tests
-> preview
-> domain pass

No blind progression is allowed.

---

## Current Outcome
The PHASE 06 operator-interactivity layer is considered canonical only if:
- its contracts remain stable
- its audit path remains visible
- its approval semantics remain preserved
- its previews remain runnable
- domain tests remain green
