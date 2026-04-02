# VISUAL TRUTH BINDING RULES v1

Status: active visual truth discipline baseline  
Scope: dashboard/HUD/view binding to canonical truth and live runtime truth  
Rule: visual layers may render, summarize, and explain truth, but may never invent it

---

## 1. Purpose

This document defines how visual layers must bind to truth.

It exists to prevent the following failures:

- beautiful but false dashboards
- guessed runtime state
- silent collapse of canonical truth and live runtime truth
- display-led architecture drift
- explainability panels that are not evidence-backed

---

## 2. Core Principle

Visual output is downstream.

This means:

- visual layers do not own truth
- visual layers do not redefine truth
- visual layers do not create authority
- visual layers do not guess missing runtime state

Visual layers may only:

- read
- compose
- map
- summarize
- explain
- render

---

## 3. Truth Sources Allowed for Visual Binding

Visual layers may bind only to the following truth classes:

### 3.1 Canonical truth
Examples:
- contracts
- canonical models
- policy definitions
- canonical IDs
- documented architecture rules

### 3.2 Live runtime truth
Examples:
- runtime status
- pressure state
- queue state
- worker state
- node health
- incident state
- topology state

### 3.3 Derived read-only views
Examples:
- panel summaries
- dashboard read models
- explainability summaries
- topology/read-only visual compositions
- HUD preview/render state contracts

### Rule

If a visual element cannot be traced back to one of these classes, it must not be shown as truth.

---

## 4. Forbidden Visual Behaviors

Visual layers must not:

- invent healthy/alive/degraded states
- invent approval status
- invent policy outcomes
- invent runtime activity
- invent queue depth
- invent node health
- invent incident severity
- invent traceability labels
- smooth over uncertainty as certainty
- display guessed state for aesthetic completeness

---

## 5. Binding Hierarchy

Visual binding must follow this order:

1. canonical definition
2. live runtime fact
3. derived read-only interpretation
4. visual mapping
5. rendered output

### Rule

Rendered output must never bypass this order.

---

## 6. Visual Mapping Rule

A visual mapping layer may decide:

- panel placement
- visual card type
- zone targeting
- icon slot
- priority
- density mode
- overlay participation
- explainability placement

But it may not decide:

- what is true
- what is healthy
- what is approved
- what is executing
- what is safe

Those must come from upstream truth.

---

## 7. Explainability Rule

Explainability panels and sidebars must be evidence-backed.

Allowed:
- summaries of upstream truth
- reason strings derived from policy/runtime/view models
- downstream explanation of system state
- traceable decision descriptions

Forbidden:
- decorative reasoning with no source
- made-up safety explanation
- UI-generated confidence with no contract/runtime basis

---

## 8. Signal Overlay Rule

Signal overlays may visualize:

- flow participation
- routing paths
- active/inactive binding
- topology participation
- highlighted vs passive paths

But overlays must not imply execution or health beyond what upstream truth supports.

### Rule

A glowing line is not proof of actual execution unless bound to an allowed upstream signal.

---

## 9. Topology Overlay Rule

Topology overlays may render:

- node grouping
- runtime relationship summaries
- display-target placement
- route visibility
- surface grouping

But they must not claim:
- physical truth they do not possess
- network trust that is not explicitly modeled
- node capability they cannot trace to source-of-truth layers

---

## 10. HUD Composition Rule

HUD composition is read-only orchestration of visual parts.

It may:
- assemble layers
- compose screen parts
- group explainability/status/sidebar/ticker regions
- expose preview/snapshot/render-ready states

It may not:
- mutate runtime state
- mutate canonical truth
- act as execution control
- become approval authority

---

## 11. Status Bar Rule

Status bars and bottom tickers must show only evidence-backed status.

Allowed:
- known labels
- upstream counters
- approved summaries
- stable truth-backed indicators

Forbidden:
- guessed “optimal”
- guessed “stable”
- guessed “secure”
- guessed “healthy”

unless those words are explicitly bound to upstream truth definitions.

---

## 12. Placeholder Rule

If truth is missing, visual layers must prefer:

- unknown
- unavailable
- pending
- not_bound
- no_runtime_signal

over false certainty.

### Rule

Explicit incompleteness is safer than elegant deception.

---

## 13. Aesthetic Rule

Beauty is allowed.
False beauty is not.

This means:
- glass panels are allowed
- glow is allowed
- depth is allowed
- animation is allowed
- motion is allowed later
- premium styling is allowed later

But none of these may distort truth binding.

---

## 14. Client Surface Rule

Desktop, mobile, shell, and future client surfaces must obey the same truth discipline.

No client surface may:
- become a secret truth owner
- display bypass state
- invent hidden execution status
- bypass control-plane/policy/validation layers

---

## 15. Visual-to-Truth Traceability Rule

Every meaningful visual state should be traceable to an upstream source.

Examples:
- panel_id -> panel metadata / source binding / read model
- overlay state -> visual mapping / panel chain / runtime participation
- explainability text -> policy/runtime/summary source
- screen state -> preview/snapshot/render contracts

### Rule

Traceability is mandatory for production-grade visual truth.

---

## 16. Pre-Polish Rule

Premium visual polish must not begin before:

- architecture/source-of-truth docs exist
- naming drift is documented
- duplicate concept watchpoints are documented
- visual truth bindings are documented
- visual state chain is stable enough to support styling without semantic drift

---

## 17. Final Operational Rule

Before adding a new panel, overlay, screen effect, or display behavior:

1. identify upstream truth source
2. identify truth class
3. identify derived binding path
4. confirm read-only behavior
5. only then render

---

## 18. Status

This document is the active visual truth discipline baseline until replaced by a stricter display/runtime binding standard.
