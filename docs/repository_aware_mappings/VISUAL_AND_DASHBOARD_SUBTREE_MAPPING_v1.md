# VISUAL AND DASHBOARD SUBTREE MAPPING v1

Status: active canonical visual/dashboard subtree mapping
Scope: repository-aware mapping for operator-facing visual and dashboard-oriented areas
Rule: visual and dashboard subtrees must remain structurally explainable so presentation meaning stays readable as downstream visibility rather than hidden authority

---

## 1. Purpose

This document defines the current repository-aware mapping for visual and dashboard-oriented subtrees.

It exists to preserve clarity about:
- where operator-facing presentation logic lives
- how visual layers differ from runtime and observability layers
- why dashboard structure should remain repository-visible

---

## 2. Visual/Dashboard Mapping Principle

Visual and dashboard-oriented areas should remain understandable in terms of:
- operator-facing visibility
- panel and view semantics
- display and presentation split
- structured downstream explanation
- future renderer and visual-shell realization

These areas should not become hidden control roots.

---

## 3. Mapping Intent

This mapping should help the operator or future engineer explain:
- where dashboard meaning lives in the repo
- how visual layers depend on upstream runtime and observability meaning
- why presentation logic remains downstream and non-authoritative

---

## 4. Required Rule

Visual and dashboard subtree interpretation should remain:
- explicit
- semantics-aware
- downstream
- distinct from runtime execution and canonical truth ownership

---

## 5. What Is Forbidden

The following remain forbidden:
- visual areas interpreted only as aesthetic code
- dashboard layers treated as authority owners
- presentation logic silently replacing system meaning
- visual structure dissolved into generic UI clutter

---

## 6. Final Rule

Visual and dashboard subtrees must remain repository-visible as structured operator-facing layers, not decorative leftovers.

---

## 7. Status

This document is the active canonical visual/dashboard subtree mapping until replaced by a stricter repository-aware dashboard map.
