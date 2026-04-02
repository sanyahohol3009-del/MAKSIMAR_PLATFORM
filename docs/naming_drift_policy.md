# NAMING DRIFT POLICY v1

Status: active repository naming policy baseline  
Scope: directory naming styles, tolerated drift, normalization boundaries  
Rule: naming variation is allowed only when architectural meaning remains explicit and documented

---

## 1. Purpose

This document defines how naming variation inside the repository must be interpreted.

The repository currently includes multiple naming styles, including:

- UPPERCASE directory names
- snake_case feature directories
- mixed server/runtime/core subtrees
- shell/client surfaces
- layer-oriented expansion directories

This is not automatically an error.

It becomes a problem only when naming drift starts hiding architectural meaning.

---

## 2. Core Rule

Naming is subordinate to architecture.

This means:

- a clear architecture with mixed naming is acceptable
- a blurred architecture with “clean” naming is not acceptable

No naming cleanup is allowed if it destroys meaning, history, traceability, or migration safety.

---

## 3. Accepted Naming Classes

## 3.1 UPPERCASE repository surfaces

Examples:

- `MAKSIMAR_CORE_LIB`
- `MAKSIMAR_SERVER`
- `CONTROL_PLANE`
- `CORE_ROOT`
- `RUNTIME`
- `SUPERVISOR`
- `DOMAIN_CUBES`
- `VOICE_LAYER`

### Meaning

UPPERCASE directory names are acceptable when they represent:

- major architecture surfaces
- platform zones
- trust/safety boundaries
- shell surfaces
- broad domain/layer surfaces
- top-level structural regions

### Rule

UPPERCASE is valid for high-level architectural regions.

---

## 3.2 snake_case feature directories

Examples:

- `ai_services`
- `voice_layer`
- `runtime_observability`
- `panel_metadata_contract.py`
- `visual_hud_preview_state_contract.py`

### Meaning

snake_case is acceptable when it represents:

- feature packages
- implementation-level modules
- contracts/models/builders
- lower-level capability packages
- internal substructure within canonical surfaces

### Rule

snake_case is valid for internal package/module structure.

---

## 3.3 Mixed style by depth

The repository may contain:

- UPPERCASE at top-level
- snake_case inside canonical packages
- UPPERCASE server/runtime regions with snake_case internals

This is acceptable if the style difference corresponds to architecture depth.

---

## 4. What Counts as Dangerous Naming Drift

Naming drift becomes dangerous when:

- names stop indicating scope or authority
- two similarly named regions imply the same ownership but actually differ
- a runtime folder looks canonical
- a canonical folder looks disposable
- a shell/client surface looks like an architecture root
- a temporary name becomes permanent without documentation

---

## 5. What Does Not Count as Dangerous Drift

The following are not automatically problems:

- `AI_SERVICES` and `MAKSIMAR_CORE_LIB/ai_services`
- `VOICE_LAYER` and `MAKSIMAR_CORE_LIB/voice_layer`
- `OBSERVABILITY_LAYER` and `MAKSIMAR_SERVER/OBSERVABILITY`
- mixed UPPERCASE and snake_case across different architecture depths

These are watchpoints, not emergency triggers.

---

## 6. Normalization Rule

Normalization may happen later, but only if all of the following are true:

1. the architectural owner is known
2. the role of the directory is documented
3. migration impact is reviewed
4. imports/paths are accounted for
5. tests pass before and after
6. no truth boundary is obscured

### Mandatory migration sequence

**proposal → naming role review → impact analysis → diff → tests → apply**

---

## 7. Temporary Names Rule

Temporary naming is dangerous.

Names such as:
- placeholder
- temp
- legacy_new
- draft_final
- new2
- misc

must not become long-term architecture surfaces.

### Rule

If a name starts behaving like a durable architecture surface, it must either:
- be documented as intentional, or
- be formally migrated later

---

## 8. Truth Boundary Naming Rule

Names should help distinguish:

- canonical truth
- runtime truth
- derived read-only view
- shell/client surface
- research/experimental surface

A name must not imply higher authority than the directory actually has.

---

## 9. Visual / Dashboard Naming Rule

Current visual/dashboard naming must remain:

- contract-driven
- traceable
- panel/view/screen/render oriented
- downstream from truth/state ownership

### Rule

Visual naming must not drift into pretending to be runtime authority.

Examples of acceptable visual naming:
- `visual_hud_preview_state_contract.py`
- `panel_to_visual_mapping_contract.py`
- `visual_signal_overlay_contract.py`

These correctly describe downstream visual/read-model responsibility.

---

## 10. Shell Naming Rule

Shell surfaces such as:

- `ANDROID_SHELL`
- `DESKTOP_SHELL`
- `IOS_SHELL`
- `SERVER_SHELL`

must remain visibly shell/client surfaces.

They must not be renamed or treated as alternate platform roots.

---

## 11. Layer Naming Rule

`*_LAYER` directories remain valid as broad domain or expansion surfaces.

They are not automatically equal to:
- canonical package owners
- runtime owners
- registry owners

### Rule

A layer name indicates program/domain scope, not automatic truth ownership.

---

## 12. Documentation-First Rule

If naming ambiguity appears, the first response is:

- document
- classify
- map ownership
- test assumptions

Not:
- rename immediately
- collapse directories
- delete structure

---

## 13. Current Policy

At the current project stage:

- mixed naming is tolerated
- architecture meaning has priority over stylistic uniformity
- documentation-first is preferred over cleanup-first
- normalization is postponed unless correctness requires it

---

## 14. Future Work

Possible future documents:

- concept ownership matrix
- naming normalization candidate list
- legacy naming migration plan
- canonical package boundary index

But not before current stabilization goals are complete.

---

## 15. Status

This document is the active naming interpretation baseline until replaced by a stricter normalization plan.
