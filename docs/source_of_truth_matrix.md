# SOURCE OF TRUTH MATRIX v1

Status: active architectural truth boundary  
Scope: canonical truth, live runtime truth, derived view boundaries, display/read-only discipline  
Rule: no layer may redefine truth outside its authority boundary

---

## 1. Core Principle

The platform must never mix:

- canonical truth
- live runtime state
- derived read-only views
- presentation output
- exploratory/research output

These are separate classes of truth and must stay separated.

---

## 2. Truth Classes

## 2.1 Canonical Truth

Canonical truth is the stable architecture-defining layer.

Examples:
- contracts
- canonical models
- validators
- builders
- policy definitions
- canonical registries
- architecture maps
- stable ID vocabulary

Primary locations:
- `MAKSIMAR_CORE_LIB`
- approved architecture documents in `docs/`

### Rule

Canonical truth:
- defines shape
- defines rules
- defines allowed meaning
- does not pretend to be live state

---

## 2.2 Live Runtime Truth

Live runtime truth is the actual operational state of the system while running.

Examples:
- process state
- queue depth
- runtime health
- worker state
- node runtime state
- pressure state
- live incidents
- live metrics
- live topology signals

Primary locations:
- `MAKSIMAR_SERVER`
- `RUNTIME`
- downstream runtime state surfaces

### Rule

Live runtime truth:
- is operational
- can change continuously
- must not overwrite canonical meaning
- must not be guessed by UI

---

## 2.3 Derived Read-Only Views

Derived read-only views are downstream interpretations of canonical truth and/or runtime truth.

Examples:
- dashboard read models
- panel content views
- explainability summaries
- topology views
- status summaries
- HUD preview/snapshot/render contracts

Primary locations:
- `MAKSIMAR_CORE_LIB/oob_dashboard`
- `MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS`
- other downstream read-only presentation contracts

### Rule

Derived views:
- may summarize
- may transform for readability
- may group signals
- may not invent state
- may not become source-of-truth owners

---

## 2.4 Presentation Truth

Presentation truth is what is shown to the operator.

Examples:
- HUD panels
- status bars
- explainability sidebars
- bottom ticker
- client screens
- display-target output

### Rule

Presentation truth is not independent truth.
It is a downstream projection and must remain traceable to:
- canonical truth
- live runtime truth
- derived read-only views

---

## 2.5 Research / Exploratory Output

Research, simulation, experimental, or hypothesis output is not production truth.

Examples:
- exploratory simulations
- candidate evaluations
- research displays
- hypothesis reports
- experimental backends
- non-validated optics/physics outputs

### Rule

Research output is not production truth until passed through strict validation and explicit approval.

---

## 3. Source-of-Truth Ownership Matrix

| Truth Class | Owner | Can Define Rules | Can Change Live | Can Drive UI | Can Apply Actions |
|---|---|---:|---:|---:|---:|
| Canonical Truth | CORE_LIB / approved docs | Yes | No | Indirectly | No |
| Live Runtime Truth | SERVER / RUNTIME | No | Yes | Indirectly | Indirectly through policy path |
| Derived Read-Only Views | Dashboard/read model layers | No | No | Yes | No |
| Presentation Output | UI/display layers | No | No | Yes | No |
| Research Output | Research/simulation layers | No | No | Optional | No |

---

## 4. Hard Boundaries

## 4.1 UI must not guess runtime truth

Dashboard, mobile, voice, and display surfaces must not invent:
- alive/dead/degraded state
- queue state
- worker state
- approval state
- incident severity

They may only display downstream truth from allowed sources.

## 4.2 Canonical truth must not be polluted by runtime facts

Contracts and canonical models must not absorb:
- transient runtime noise
- backend-specific hacks
- guessed health signals
- UI presentation hacks

## 4.3 Runtime must not redefine canonical meaning

Runtime layers may produce live facts, but may not silently redefine:
- policy meaning
- canonical ID meaning
- contract meaning
- trust-boundary meaning

## 4.4 Presentation must remain read-only

Visual/HUD layers:
- read
- render
- explain

They do not:
- mutate canonical truth
- mutate runtime truth
- bypass control plane
- bypass policy/validation/execution control

---

## 5. JARVIS Access Rule

Future broad-access JARVIS read scope may include:
- project files
- repositories
- documents
- chats/archives
- drive/email context
- code structure
- dependency structure
- system/project metadata

But this does not change truth ownership.

### Rule

Broad read access does not grant:
- truth authorship
- direct apply rights
- direct publish rights
- direct delete rights
- direct execution bypass

---

## 6. Agent Helper Rule

Future agent/helper/swarm cubes may:
- read canonical truth
- read runtime truth
- build derived reports
- generate proposals
- suggest patches
- operate in sandbox

They may not:
- redefine source-of-truth ownership
- bypass approval
- replace control plane
- become canonical truth owners

---

## 7. Observability Rule

Observability must expose truth boundaries clearly.

Observability may show:
- where canonical definition lives
- where live runtime fact lives
- where derived summary came from
- whether a UI panel is direct, derived, or explainable-only

### Rule

Observability is required to improve traceability, not to flatten truth classes into one layer.

---

## 8. Visual / HUD Rule

Current HUD work must obey:

- HUD is downstream
- HUD is read-only
- HUD does not fabricate runtime state
- HUD does not collapse canonical truth and runtime truth into one blob
- HUD remains explainable and traceable

This means:
- beauty never outranks truth
- clean UI never justifies false UI
- display state must remain evidence-backed

---

## 9. Network / Trust Zone Rule

DEV / HOME / MOBILE / display sync / memory sync / export paths must not collapse into one trust zone for convenience.

### Rule

Truth transport and truth ownership are different concerns.
Moving data across nodes does not transfer authority automatically.

---

## 10. Final Operational Rule

Before any future refactor, dashboard enhancement, agent integration, or runtime expansion:

1. identify truth class
2. identify owner
3. identify downstream readers
4. confirm no boundary crossing
5. only then implement

---

## 11. Status

This document is the active truth-boundary baseline until replaced by a stricter per-domain source-of-truth matrix.
