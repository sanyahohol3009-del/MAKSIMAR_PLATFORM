# CANONICAL ARCHITECTURE MAP v1

Status: active source-of-truth baseline  
Scope: repository structure, architectural intent, migration safety boundary  
Rule: this document defines the canonical interpretation of the current repository layout and must be updated before any structural migration.

---

## 1. Canonical Platform Root

These directories are the canonical platform root and represent the primary engineering baseline:

- `MAKSIMAR_CORE_LIB`
- `MAKSIMAR_SERVER`
- `tests`
- `scripts`
- `SHARED`

### Meaning

- `MAKSIMAR_CORE_LIB`  
  Canonical contracts, models, validators, builders, policy shapes, and stable architecture-facing definitions.

- `MAKSIMAR_SERVER`  
  Runtime application layer, live execution state, routing, orchestration, observability bindings, runtime health, execution control, and server-side read models.

- `tests`  
  Compile-pass and behavior validation layer for the platform.

- `scripts`  
  Controlled engineering utilities and repeatable project helper commands.

- `SHARED`  
  Cross-surface shared assets, shared integration helpers, and common cross-boundary support elements.

---

## 2. Runtime Safety Legacy

These directories remain part of the valid runtime safety and operational legacy surface:

- `CORE_ROOT`
- `CONTROL_PLANE`
- `RUNTIME`
- `SUPERVISOR`
- `SANDBOX`

### Meaning

- `CORE_ROOT`  
  Immutable or protected core authority boundary. No uncontrolled write path is allowed.

- `CONTROL_PLANE`  
  Decision and orchestration layer. Policy-aware routing and coordination belong here.

- `RUNTIME`  
  Live state, operational artifacts, runtime facts, and downstream execution-visible state.

- `SUPERVISOR`  
  Controlled supervision, process guarding, runtime safety enforcement, and lifecycle oversight.

- `SANDBOX`  
  Isolated execution and safe experimentation boundary. No direct authority over immutable core.

### Rule

These directories are not “temporary clutter.”  
They are valid architecture-bearing surfaces and must not be removed or reinterpreted casually.

---

## 3. Shell Surfaces

These directories are valid shell/client surfaces:

- `ANDROID_SHELL`
- `DESKTOP_SHELL`
- `IOS_SHELL`
- `SERVER_SHELL`

### Meaning

Each shell surface represents a client or operator-facing integration surface and must remain downstream from platform rules.

### Rule

Shell surfaces:
- do not redefine core contracts
- do not bypass control-plane policy
- do not become alternate architecture roots

---

## 4. Domain and Product Surfaces

These repository regions are valid domain/product expansion surfaces:

- `*_LAYER`
- `DOMAIN_CUBES`

### Meaning

- `*_LAYER` directories represent domain-specific or capability-specific expansion regions.
- `DOMAIN_CUBES` represents modular product/capability units intended to plug into the broader platform.

### Rule

New business/domain functionality should enter through module/cube/layer logic rather than by mutating platform root structure.

---

## 5. Migration Rule

Nothing may be deleted, relocated, or reclassified without this sequence:

**proposal → impact review → diff → tests → apply**

### Mandatory implications

- no spontaneous structural cleanup
- no “looks redundant, delete later” behavior
- no directory movement without architectural justification
- no migration without compile-pass and test confirmation

---

## 6. Naming Drift Policy

The repository currently contains a mixture of naming styles, including:

- UPPERCASE directories
- snake_case feature directories
- feature-specific runtime/server/core subtrees

This is currently acceptable **only because it is explicit and tracked**.

### Rule

Naming variation is tolerated only while:
- architecture meaning stays clear
- source-of-truth interpretation is documented
- no silent reclassification occurs

### Future note

A normalization pass may happen later, but not during active foundation stabilization unless required by correctness.

---

## 7. Duplicate Concept Watchpoints

The following concept groups require source-of-truth discipline and must be treated as watchpoints:

### 7.1 AI services

- `AI_SERVICES`
- `MAKSIMAR_CORE_LIB/ai_services`

### 7.2 Voice surfaces

- `VOICE_LAYER`
- `MAKSIMAR_CORE_LIB/voice_layer`
- `MAKSIMAR_SERVER/VOICE_*`

### 7.3 Observability surfaces

- `OBSERVABILITY_LAYER`
- `MAKSIMAR_CORE_LIB/runtime_observability`
- `MAKSIMAR_CORE_LIB/observability_contracts`
- `MAKSIMAR_SERVER/OBSERVABILITY`

### Rule

These are not automatically errors.  
They are **source-of-truth matrix candidates** and must be interpreted deliberately before any cleanup or merge action.

---

## 8. Visual / Operator Track Boundary

The current visual/operator work is valid only if it remains:

- contract-driven
- read-only at dashboard level
- downstream from platform rules
- separate from execution authority
- separate from core mutation rights

### Rule

Visual polish must not start before:
- canonical architecture/source-of-truth mapping is formalized
- observability extension boundaries are understood
- visual state bindings are stabilized

---

## 9. Agent Helper Integration Boundary

Future agent/helper/swarm systems must enter as:

- cube/module/helper surface
- policy-bound actor
- dashboard-exposed component
- approval-controlled assistant

They must not enter as:
- replacement core
- alternate platform root
- uncontrolled autonomous writer

### Rule

Platform dresses the module.  
The module does not redefine the platform.

---

## 10. Current Interpretation

Current repository state is acceptable as a growing architecture **if interpreted through this map**.

This means:
- platform root remains canonical
- runtime safety legacy remains valid
- shell surfaces remain downstream
- domain/product surfaces remain modular
- naming drift is watched, not ignored
- duplicate concepts are tracked as matrix candidates, not panic triggers

---

## 11. Operational Rule

Before any future structural cleanup, migration, merge, or large refactor:

1. update this file if meaning changes
2. define impact boundary
3. produce diff
4. run tests
5. only then apply

---

## 12. Status

This document is the active repository structure truth baseline until replaced by a stricter canonical source-of-truth matrix.
