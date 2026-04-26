# JARVIS PHASE 07 — BASE PANEL CONTENT CANONICAL

## Status
This document fixes the canonical state of PHASE 07 for the dashboard/operator domain.

Current confirmed status:
- PHASE 7A — System Status Panel: closed
- PHASE 7B — Guard Chain Panel: closed
- PHASE 7C — Incidents Panel: closed
- PHASE 7D — Logs Panel: closed
- PHASE 7E — Topology Panel: closed

PHASE 07 is considered operator-ready and canonical-ready for JARVIS internal understanding.

---

## Purpose of PHASE 07
PHASE 07 formalizes the base panel-content layer for the foundation dashboard.

This phase exists to ensure that each base panel is no longer only a panel id or binding target, but a complete canonical content layer with:
- content contract
- payload builder
- fixture set
- terminal preview
- local web preview
- tests
- manual acceptance semantics

This phase does not introduce execution powers.
This phase does not move truth into UI.
This phase does not bypass any governance, control, or audit path.

---

## Canonical Panels Closed in PHASE 07

### 1. System Status Panel
Canonical files:
- system_status_panel_content_contract.py
- system_status_panel_payload_builder.py
- fixtures/system_status_*.json
- system_status_panel_terminal_preview.py
- system_status_panel_web_preview.py

Purpose:
- expose foundation runtime summary state
- preserve visible status vocabulary
- preserve read-only operator visibility
- distinguish normal / empty / degraded / incident / stale / loading

Load-bearing semantics:
- runtime summary must be readable
- degraded must remain visible
- stale must not be hidden
- panel stays read-only
- panel stays visible in main dashboard and OOB

### 2. Guard Chain Panel
Canonical files:
- guard_chain_panel_content_contract.py
- guard_chain_panel_payload_builder.py
- fixtures/guard_chain_*.json
- guard_chain_panel_terminal_preview.py
- guard_chain_panel_web_preview.py

Purpose:
- expose canonical guard-chain structure
- preserve runtime / guard / core_guard / kernel_guard presence
- preserve chain-health readability

Load-bearing semantics:
- runtime_entry_present
- guard_entry_present
- core_guard_entry_present
- kernel_guard_entry_present
- derived state must remain explicit
- panel stays read-only and operator-visible

### 3. Incidents Panel
Canonical files:
- incidents_panel_content_contract.py
- incidents_panel_payload_builder.py
- fixtures/incidents_*.json
- incidents_panel_terminal_preview.py
- incidents_panel_web_preview.py

Purpose:
- expose active incidents, history visibility, severity, and lifecycle

Load-bearing semantics:
- current incident visibility
- history-visible incident path
- severity bucket readability
- kill-chain-triggered visibility
- panel stays read-only and operator-visible

### 4. Logs Panel
Canonical files:
- logs_panel_content_contract.py
- logs_panel_payload_builder.py
- fixtures/logs_*.json
- logs_panel_terminal_preview.py
- logs_panel_web_preview.py

Purpose:
- expose diagnostics/log-tail semantics for operator visibility

Load-bearing semantics:
- diagnostics correlation readability
- severity bucket readability
- source-file visibility
- failure visibility
- stalled-stage visibility
- panel stays read-only and operator-visible

### 5. Topology Panel
Canonical files:
- topology_panel_content_contract.py
- topology_panel_payload_builder.py
- fixtures/topology_*.json
- topology_panel_terminal_preview.py
- topology_panel_web_preview.py

Purpose:
- expose canonical foundation topology
- preserve runtime / guard / core_guard / kernel_guard topology shape
- preserve topology relationships and startup-order semantics

Load-bearing semantics:
- exactly one node each for runtime / guard / core_guard / kernel_guard
- topology relationships remain explicit
- topology state is derived from foundation truth layers
- panel stays read-only and operator-visible

---

## Canonical State Vocabulary Introduced in PHASE 07
Across the base panel layer, the canonical visible state vocabulary is:

- normal
- empty
- degraded
- incident
- stale
- loading

This vocabulary must remain explicit.
No panel may silently collapse these into a generic status.

---

## Canonical Development Pattern Fixed in PHASE 07
Every base panel in PHASE 07 follows the same pattern:

contract
-> payload builder
-> fixtures
-> terminal preview
-> local web preview
-> tests
-> operator-ready acceptance

This pattern is now canonical for future dashboard panel work.

---

## Source-of-Truth Rule
Base panel content must remain derived from canonical upstream truth layers.

Examples:
- system_status -> foundation unified / live-historical / truth consistency
- guard_chain -> guard-chain truth + foundation views
- incidents -> foundation incident dashboard view
- logs -> foundation diagnostics correlation view
- topology -> foundation unified + live-historical + truth consistency

A panel may expose truth.
A panel may not become the truth source.

---

## Invariants That Must Not Be Broken

1. All PHASE 07 base panels remain read-only.
2. All PHASE 07 base panels remain operator-visible.
3. All PHASE 07 base panels remain visible in main dashboard and OOB where defined.
4. Payload builders must remain downstream of canonical content contracts.
5. Fixtures must remain available for shape/state testing.
6. Terminal preview must remain runnable.
7. Local web preview must remain runnable.
8. State vocabulary must remain explicit.
9. Derived state must remain derived from truth layers, not hardcoded UI-local guesses.
10. No base panel gains direct execution ability.

---

## Forbidden Changes
The following are forbidden:
- turning a PHASE 07 panel into an action executor
- hiding degraded / stale / incident states
- replacing upstream truth with local UI state
- removing preview discipline
- removing fixtures
- collapsing canonical state vocabulary into one generic status
- inventing alternative topology / incident / logs truth paths
- introducing non-canonical shortcuts only to satisfy tests

---

## Safe Future Extension Zones
The following extensions are allowed on top of PHASE 07:
- richer payload fields
- richer previews
- richer web/local visualization
- panel overlays
- explainability additions
- mobile/dashboard projection
- voice/gesture exposure
- future renderer bindings

Provided that:
- panel remains read-only unless explicitly moved into a governed interaction layer
- canonical truth remains upstream
- tests remain green
- previews remain runnable

---

## JARVIS Rule for Future Panel Growth
If JARVIS extends any PHASE 07 panel, it must preserve:

contract
-> payload builder
-> fixtures
-> preview
-> tests
-> domain pass

If any one of these is missing, the extension is not canonical.

---

## Outcome of PHASE 07
PHASE 07 establishes the canonical base-content layer for the foundation dashboard.

This means:
- the dashboard now has canonical panel content, not just panel ids
- JARVIS can read the dashboard layer as structured content
- future visualization can grow on top of stable panel contracts
- future renderer work is less likely to drift away from platform truth
