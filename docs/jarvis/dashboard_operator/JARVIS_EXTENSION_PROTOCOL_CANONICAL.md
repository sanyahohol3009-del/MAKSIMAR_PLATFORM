# JARVIS EXTENSION PROTOCOL CANONICAL

## Purpose
This document defines how JARVIS may extend the dashboard/operator platform safely.

The goal is:
- allow future growth
- avoid architectural drift
- avoid blocking future improvement
- preserve governance, audit, and control boundaries

This is the canonical extension protocol for:
- buttons
- functions
- panels
- operator surfaces
- dashboard views
- modules
- cubes
- voice/gesture/dashboard entry points

---

## Core Principle
Extension is allowed.
Unbounded uncontrolled mutation is not allowed.

JARVIS must treat extension as controlled growth, not as permission to rewrite the platform.

---

## Canonical Extension Pipeline
Every new extension must follow:

contract
-> models/read-model
-> contract builder
-> tests
-> preview
-> domain pass

No step may be skipped.

---

## Hard Boundaries That Must Never Be Broken

### 1. UI does not execute
A dashboard button, surface, or panel may expose intent or state.
It may not perform direct execution.

Correct path:
UI
-> intent
-> control-plane
-> policy
-> approval
-> execution

### 2. No bypass of approval/policy
Any control-like extension must preserve:
- approval_required
- policy_gate_required
- audit visibility

### 3. No write upward into immutable truth
An extension may not mutate:
- immutable core truth
- canonical operator truth
- canonical audit truth
- canonical display truth
outside approved downstream flows

### 4. No hidden audit path
If an action enters operator flow, it must remain visible through canonical audit semantics.

### 5. No hardcoded alternative routing world
A new feature may not create:
- a second control plane
- a second dashboard truth model
- a second hidden display-routing path
- a second approval semantics path

### 6. Canonical ids must remain stable
Stable ids must not be casually renamed.
New ids must be introduced through controlled canonical vocabulary.

---

## What JARVIS May Add Safely

JARVIS may add:
- new dashboard buttons
- new panel contracts
- new panel content contracts
- new operator surfaces
- new queue views
- new approval views
- new audit views
- new module panels
- new cube bindings
- new mobile/voice/gesture bindings
- new display-targeted panel exposure
- new previews and validation surfaces

Provided that canonical boundaries remain intact.

---

## How to Add a New Button
A button is not a direct action.

Correct process:
1. define the button intent contract
2. bind it to canonical operator/dashboard semantics
3. ensure it routes into control-plane handoff
4. ensure approval/policy path is preserved if applicable
5. ensure audit visibility remains preserved
6. add tests
7. add preview
8. run domain tests

A button may expose:
- read-only request
- navigation request
- control request

But it must never directly execute logic.

---

## How to Add a New Function
A function may be added only if its execution class is clear.

### Read-only function
Allowed if it:
- reads canonical truth
- does not mutate state
- remains operator-visible
- passes tests and preview

### Control function
Allowed only if it:
- declares approval requirement
- declares policy gate path
- remains audit-visible
- enters guarded handoff path
- never bypasses downstream governance

---

## How to Add a New Panel
A new panel must be added through:
1. panel id
2. panel metadata
3. panel source binding
4. panel content contract
5. panel/view/display binding
6. tests
7. preview
8. domain pass

A panel may not invent its own source of truth.

---

## How to Add a New Operator Surface
A new interaction surface must:
- derive from canonical read-model truth
- preserve approval/read-only distinction where relevant
- preserve forbidden-state visibility
- preserve disabled-state visibility
- preserve audit visibility
- preserve traceability

A new surface may not become a new control-plane substitute.

---

## How to Add a New Module or Cube
A module or cube must be attached through:
- manifest
- canonical id
- permission / policy binding
- panel surface or dashboard exposure
- tests
- preview
- domain pass

A cube must not rewrite stable platform truth.

---

## Safe Extension Zones
The following are open for controlled growth:
- dashboards
- panels
- queue views
- audit views
- module surfaces
- mobile surfaces
- gesture/voice surfaces
- display presentation
- preview layers
- explainability overlays

These are safe because they are downstream expression layers.

---

## Restricted Zones
The following are not free mutation zones:
- immutable core
- control-plane semantics
- approval semantics
- audit semantics
- canonical id vocabulary
- stable truth contracts
- stop-gate / guard / halt authority

Any change here requires stricter governance.

---

## Rule for Future JARVIS Self-Extension
JARVIS may extend the system only if all of the following remain true:
- truth contracts stay canonical
- direct execution is not introduced
- approval semantics remain preserved
- audit visibility remains preserved
- operator-visible state remains explicit
- previews remain runnable
- domain tests remain green

If any of these fail, the extension is not canonical.

---

## Minimal Decision Rule
Before JARVIS adds anything new, it must answer:

1. What contract is the source of truth?
2. Is this read-only or control-like?
3. Does approval apply?
4. Does audit visibility apply?
5. Does this create a second routing world?
6. Can it be previewed?
7. Can it pass domain tests?

If the answer is incomplete, extension must stop until clarified.
