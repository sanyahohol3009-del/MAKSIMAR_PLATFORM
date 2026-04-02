# DUPLICATE CONCEPTS MATRIX v1

Status: active architectural interpretation document  
Scope: concept groups with multiple repository surfaces  
Rule: duplicate concept presence is not automatically an error; each concept group must be interpreted by role

---

## 1. Purpose

This document exists to prevent false cleanup, panic refactors, and architectural drift caused by seeing the same concept name in multiple places.

A repeated concept across the repository may mean:

- canonical contract layer
- runtime implementation layer
- legacy compatibility layer
- shell/client exposure layer
- future expansion slot
- research/experimental surface

The existence of multiple concept surfaces is acceptable only if their roles are explicit.

---

## 2. Interpretation Rule

When the same concept appears in multiple repository regions, the correct response is:

1. identify each surface
2. classify its role
3. define which one is canonical
4. define which ones are downstream
5. define which ones are legacy/watchpoints
6. avoid cleanup until impact is understood

---

## 3. Concept Group: AI Services

### Surfaces

- `AI_SERVICES`
- `MAKSIMAR_CORE_LIB/ai_services`

### Interpretation

- `MAKSIMAR_CORE_LIB/ai_services`
  Canonical contract/model/registry-facing AI service definition layer.

- `AI_SERVICES`
  Repository-level service surface / integration slot / deployment-facing or future runtime-facing AI services region.

### Current rule

These are not duplicates in the destructive sense.
They represent different architecture levels.

### Risk

Risk appears only if:
- runtime implementation starts redefining canonical contracts
- repository-level service surfaces become alternate truth owners

### Current status

Watchpoint, not emergency.

---

## 4. Concept Group: Voice

### Surfaces

- `VOICE_LAYER`
- `MAKSIMAR_CORE_LIB/voice_layer`
- `MAKSIMAR_SERVER/VOICE_*`

### Interpretation

- `MAKSIMAR_CORE_LIB/voice_layer`
  Canonical voice contracts/models/registries.

- `MAKSIMAR_SERVER/VOICE_*`
  Server-side runtime/flow/integration implementations for voice-related execution.

- `VOICE_LAYER`
  High-level repository expansion/domain surface for voice track.

### Current rule

Voice must remain split as:
- canonical definitions
- runtime realization
- broader domain/program surface

### Risk

Risk appears if:
- VOICE_LAYER becomes an undefined parallel architecture root
- server runtime starts redefining canonical voice truth
- UI/voice path bypasses control-plane and policy

### Current status

Valid multi-surface concept group, must remain role-separated.

---

## 5. Concept Group: Observability

### Surfaces

- `OBSERVABILITY_LAYER`
- `MAKSIMAR_CORE_LIB/runtime_observability`
- `MAKSIMAR_CORE_LIB/observability_contracts`
- `MAKSIMAR_SERVER/OBSERVABILITY`

### Interpretation

- `MAKSIMAR_CORE_LIB/observability_contracts`
  Canonical contract shapes for observability-facing data.

- `MAKSIMAR_CORE_LIB/runtime_observability`
  Runtime-oriented observability model/contract layer within core library scope.

- `MAKSIMAR_SERVER/OBSERVABILITY`
  Server-side live observability realization and runtime metric/trace/incident surfaces.

- `OBSERVABILITY_LAYER`
  High-level repository observability program surface / future expansion slot.

### Current rule

Observability should be interpreted as a layered stack, not as redundant clutter.

### Recommended mental split

- base observability contracts
- runtime observability contracts/models
- server-side live observability realization
- top-level observability expansion/program surface

### Risk

Risk appears if:
- contracts and live metrics collapse into one mixed truth class
- top-level observability layer becomes vague and unbounded
- UI invents observability state without traceable source

### Current status

Legitimate multi-surface stack. Requires discipline, not deletion.

---

## 6. Concept Group: Dashboard / Visual / UI

### Surfaces

- `UI_LAYER`
- `VISUAL_ENGINEERING_LAYER`
- `DESKTOP_SHELL`
- `ANDROID_SHELL`
- `IOS_SHELL`
- `MAKSIMAR_CORE_LIB/oob_dashboard`

### Interpretation

- `MAKSIMAR_CORE_LIB/oob_dashboard`
  Canonical dashboard/view/panel/display-facing contracts and read-only composition logic.

- `UI_LAYER`
  Broader repository UI/domain expansion surface.

- `VISUAL_ENGINEERING_LAYER`
  Visual engineering program surface.

- shell directories
  client-specific shell surfaces

### Current rule

The dashboard contract layer is not the same thing as all UI/visual/client layers.

### Risk

Risk appears if:
- shell/UI layers redefine truth
- visual styling is started before truth/state closure
- client runtime bypasses dashboard/control-plane law

### Current status

Acceptable layered split.

---

## 7. Concept Group: Control / Runtime / Safety

### Surfaces

- `CONTROL_PLANE`
- `RUNTIME`
- `SUPERVISOR`
- `CORE_ROOT`
- `SANDBOX`
- `MAKSIMAR_SERVER`
- `MAKSIMAR_CORE_LIB`

### Interpretation

This is not duplication in the naming sense.
This is the platform spine.

### Rule

These layers must be read as a structured system:
- canonical truth in CORE_LIB
- server runtime realization in SERVER
- control-plane orchestration in CONTROL_PLANE
- live state in RUNTIME
- supervision in SUPERVISOR
- immutable/protected authority in CORE_ROOT
- safe experimentation in SANDBOX

### Current status

Core structured architecture, not duplicate clutter.

---

## 8. Concept Group: Modules / Cubes / Layers

### Surfaces

- `MODULE_SYSTEM`
- `DOMAIN_CUBES`
- `*_LAYER`

### Interpretation

- `MODULE_SYSTEM`
  module/cube/plugin architecture logic surface

- `DOMAIN_CUBES`
  modular functional capability/product units

- `*_LAYER`
  broad domain/capability surfaces

### Current rule

These are related but not identical concepts.

### Risk

Risk appears if:
- modules/cubes/layers are used interchangeably without manifest/registry law
- a new feature lands in the wrong abstraction level
- product cubes start mutating core platform boundaries directly

### Current status

Needs future manifest/registry formalization, but architecture intent is valid.

---

## 9. Canonical vs Downstream Rule

For every concept group above, the question must be answered in this order:

1. Where is the canonical contract/model truth?
2. Where is the live runtime realization?
3. Where is the shell/client exposure?
4. Where is the future expansion/program surface?
5. Which surfaces are legacy/watchpoints only?

No cleanup is allowed before those answers exist.

---

## 10. No-Panic Rule

Duplicate concept presence does not justify:
- deletion
- movement
- rename
- merge
- collapse into one directory

without:

**proposal → concept role review → impact analysis → diff → tests → apply**

---

## 11. Current Operational Guidance

At the current stage of the project:

- treat duplicate concepts as role-separated architecture surfaces
- prefer documentation before refactor
- prefer matrix interpretation before cleanup
- prefer compile-pass and tests before structural action

---

## 12. Future Work

A stricter follow-up may later define:

- naming normalization matrix
- concept ownership matrix
- migration candidates list
- legacy-to-canonical transition plan

But not before current foundation stabilization is complete.

---

## 13. Status

This document is the active interpretation baseline for duplicate concept groups until replaced by a stricter concept ownership matrix.
