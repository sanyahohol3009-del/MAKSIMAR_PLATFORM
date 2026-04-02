# VISUAL POLISH ANTI-DRIFT RULE v1

Status: active  
Scope: forbidden semantic/architectural drift during visual polish  
Rule: polish refines presentation only; it must not mutate semantics, truth ownership, or runtime coupling

---

## 1. Purpose

This document defines what visual polish is not allowed to change.

It exists to prevent redesign hiding inside polish.

---

## 2. Forbidden Drift

Visual polish must not:

- change payload shape
- change semantic meaning of panel/state/status
- change truth ownership
- change control-flow meaning
- create new runtime dependencies
- create new execution pathways
- introduce new approval semantics
- introduce new hidden coupling between UI and runtime

---

## 3. Visual-Only Boundary

Allowed:
- theme refinement
- visual hierarchy refinement
- spacing/alignment refinement
- frame/border/glow/depth refinement
- readability improvement
- non-semantic motion later in controlled scope

Forbidden:
- changing what data means
- changing what state means
- changing what panel priority means unless backed by contracts
- changing execution interpretation through styling

---

## 4. Final Rule

If a change affects meaning rather than presentation, it is not polish.
It belongs to a different pass and must not enter under the name of visual refinement.
