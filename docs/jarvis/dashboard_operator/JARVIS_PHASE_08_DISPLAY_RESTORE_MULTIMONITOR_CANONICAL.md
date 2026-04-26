# JARVIS PHASE 08 — DISPLAY / RESTORE / MULTI-MONITOR CANONICAL

## Status
This document fixes the canonical state of PHASE 08 for the dashboard/operator display and restore domain.

Current confirmed status:
- PHASE 8.1 — Monitor Inventory: closed
- PHASE 8.2 — Monitor Metadata: closed
- PHASE 8.3 — Display Occupancy: closed
- PHASE 8.4 — Assignment Registry: closed
- PHASE 8.5 — Replacement Policy: closed
- PHASE 8.6 — Free Display Selection Policy: closed
- PHASE 8.7 — Conflict Resolution: closed
- PHASE 8.8 — Restore Contracts: closed

PHASE 08 is considered operator-ready and canonical-ready for JARVIS internal platform understanding.

---

## Purpose of PHASE 08
PHASE 08 formalizes the display placement, replacement, selection, conflict, and restore path for the dashboard layer.

This phase exists to make the following canonical:
- what monitor/display targets exist
- what metadata each display target exposes
- which displays are pinned or replaceable
- which assignments are active
- how replacement decisions are derived
- how free display candidates are selected
- how conflicts are resolved
- how display/workspace/panel restore remains predictable after restart

PHASE 08 does not introduce action execution.
PHASE 08 does not move truth into UI.
PHASE 08 does not create a second display-routing world.

---

## Canonical Display Target Vocabulary
PHASE 08 is normalized around these canonical display targets:

- display_foundation_primary
- display_foundation_secondary
- display_operator_interaction

These ids must remain the canonical display vocabulary for the current dashboard display layer.

No extension may introduce alternative competing ids for the same meaning.

---

## Canonical Layers Closed in PHASE 08

### 1. Monitor Inventory
Canonical purpose:
- formalize the currently supported monitor/display surfaces
- preserve multi-monitor readiness
- distinguish foundation and operator surfaces

Canonical semantics:
- foundation_primary_monitor
- foundation_secondary_monitor
- operator_interaction_monitor
- multi_monitor_capable = true
- operator_visible = true

This layer is inventory-only.
It does not replace occupancy, assignment, or restore logic.

### 2. Monitor Metadata
Canonical purpose:
- enrich monitor inventory with display metadata

Canonical semantics:
- display_role
- display_zone
- fallback_display_target_id
- occupancy_class
- assignment_count
- foundation/operator support semantics

This layer is metadata-only.
It does not replace inventory, occupancy, assignment, or resolver layers.

### 3. Display Occupancy
Canonical purpose:
- expose whether each display target is pinned or replaceable

Canonical semantics:
- occupied_pinned
- occupied_replaceable
- total_assignments
- replaceable_assignments
- pinned_assignments
- operator_visible = true

Current canonical occupancy classes:
- foundation_primary_display
- foundation_secondary_display
- operator_interaction_display

### 4. Assignment Registry
Canonical purpose:
- expose explicit display assignments and workspace bindings

Canonical semantics:
- foundation_primary_surface
- foundation_secondary_surface
- operator_interaction_surface
- display_assignment_active
- replaceable
- workspace binding
- operator_visible = true

This layer remains the canonical assignment source for downstream display logic.

### 5. Replacement Policy
Canonical purpose:
- determine whether a display target may be replaced without disruption

Canonical semantics:
- not_replaceable
- replaceable_without_disruption

Canonical replacement classes:
- foundation_primary_pinned_surface
- foundation_secondary_replaceable_surface
- operator_interaction_replaceable_surface

Meaning:
replacement is derived from occupancy and assignment truth, not invented locally.

### 6. Free Display Selection Policy
Canonical purpose:
- choose the best replaceable display candidate for auxiliary/operator placement

Canonical semantics:
- replaceable_display_candidate_available
- no_free_display_available
- replaceable_secondary_or_tertiary_available
- no_replaceable_display_available
- operator_auxiliary_surface

Meaning:
candidate selection is policy-driven and explicit.

### 7. Conflict Resolution
Canonical purpose:
- resolve display conflicts between pinned and replaceable surfaces

Canonical semantics:
- retain_pinned_surface
- replace_replaceable_surface
- foundation_primary_conflict
- foundation_secondary_conflict
- incumbent_assignment_id
- candidate_display_target_id

Meaning:
conflict handling is explicit and derived from replacement policy and candidate selection.

### 8. Restore Contracts
Canonical purpose:
- preserve predictable restore behavior across display/workspace/panel layers

Closed restore layers:
- display_assignment_restore_contract
- display_restore_continuity_contract
- workspace_restore_contract
- panel_placement_restore_contract

Canonical restore semantics:
- restore_direct
- restore_shared_surface
- restore_ready
- restore_continuity_preserved
- workspace_restore_ready
- truth_bound = true
- operator_visible = true

Meaning:
restore behavior remains explicit, traceable, and predictable.

---

## Canonical Spine of PHASE 08

display_target_vocabulary
-> monitor_inventory
-> monitor_metadata
-> display_assignment_registry
-> display_occupancy
-> display_replacement_policy
-> free_display_selection
-> display_conflict_resolution
-> display_assignment_restore
-> display_restore_continuity
-> workspace_restore
-> panel_placement_restore

This is the canonical PHASE 08 display/restore spine.

---

## Preview Discipline Fixed in PHASE 08
PHASE 08 confirms a canonical preview discipline for display/restore layers.

Each canonical layer should expose:
- contract
- tests
- terminal preview
- local web preview where applicable
- domain pass

This rule now applies to the display/restore stack as canonical engineering discipline.

---

## Source-of-Truth Rule
Display and restore layers must remain derived from canonical upstream truth.

Examples:
- monitor metadata derives from monitor inventory + display target vocabulary + occupancy
- replacement policy derives from assignment registry + occupancy
- free display selection derives from occupancy + replacement policy
- conflict resolution derives from assignment registry + replacement policy + free display selection
- restore continuity derives from display assignment restore
- workspace restore derives from workspace read model + assignment restore + restore continuity

A preview may expose truth.
A display contract may structure truth.
No display or restore layer may become an alternative truth root.

---

## Invariants That Must Not Be Broken

1. Canonical display target ids must remain stable.
2. All PHASE 08 layers remain operator-visible.
3. Inventory must remain inventory-only.
4. Metadata must remain metadata-only.
5. Occupancy must remain derived from assignment truth.
6. Replacement policy must remain derived from occupancy and assignment truth.
7. Free display selection must remain policy-driven and explicit.
8. Conflict resolution must remain explicit.
9. Restore semantics must remain explicit and predictable.
10. Restore layers must remain truth-bound.
11. No PHASE 08 layer may execute dashboard/business actions.
12. No PHASE 08 layer may create a parallel routing world.

---

## Forbidden Changes
The following are forbidden:
- inventing new display ids for current canonical surfaces
- bypassing assignment registry
- replacing occupancy truth with UI-local guesses
- making replacement policy ad hoc
- hiding conflict semantics
- implicit restore without explicit restore state
- dropping truth_bound semantics from workspace/panel restore
- introducing direct execution through display or restore layers
- rewriting the display spine into a second root display world

---

## Safe Future Extension Zones
The following are allowed in future growth:
- richer monitor metadata
- richer display topology modeling
- stronger physical monitor identity tracking
- logical display target abstraction
- stronger close/replace operator decision layers
- continuity/snapshot hardening
- richer restore simulation and replay
- multi-display scaling
- mobile / wrist / AR downstream display targets

Provided that:
- canonical ids remain stable
- downstream layers stay derived
- truth remains upstream
- tests remain green
- preview discipline remains available

---

## Relationship to Optional Hardening
Optional hardening may extend PHASE 08 with:
- display continuity snapshot
- physical monitor identity
- logical display target abstraction
- operator close/replace decision contracts

These are allowed as hardening layers on top of the canonical PHASE 08 base.
They must not replace the canonical base already closed.

---

## Outcome of PHASE 08
PHASE 08 establishes the canonical display/restore/multi-monitor layer for the dashboard platform.

This means:
- display targets are now canonicalized
- display occupancy and replacement are explicit
- auxiliary display selection is explicit
- conflict handling is explicit
- restore behavior is predictable and truth-bound
- future display scaling can grow on top of stable canonical contracts
