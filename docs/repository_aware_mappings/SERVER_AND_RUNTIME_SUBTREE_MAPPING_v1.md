# SERVER AND RUNTIME SUBTREE MAPPING v1

Status: active canonical server/runtime subtree mapping
Scope: repository-aware mapping for server, runtime, execution, and live operational layers
Rule: server and runtime subtrees must remain structurally explainable so live behavior is distinguishable from canonical and downstream-only layers

---

## 1. Purpose

This document defines the current repository-aware mapping for server and runtime-oriented subtrees.

It exists to preserve clarity about:
- where live behavior and operational logic live
- how runtime-related areas differ from core contracts
- how server and execution surfaces remain structurally understandable

---

## 2. Server/Runtime Mapping Principle

Server and runtime-oriented areas should remain understandable in terms of:
- live execution behavior
- runtime state and lifecycle logic
- operational handling
- bounded relation to core rules and downstream observability/presentation

---

## 3. Mapping Intent

This mapping should help the operator or future engineer explain:
- where execution-oriented behavior lives
- where runtime-oriented logic lives
- how these subtrees differ from canonical models and from dashboard/presentation areas

---

## 4. Required Rule

Server and runtime subtree interpretation should remain:
- explicit
- lifecycle-aware
- operationally explainable
- distinct from both core authority and downstream presentation-only logic

---

## 5. What Is Forbidden

The following remain forbidden:
- runtime areas interpreted only by path familiarity
- live execution surfaces confused with core truth ownership
- presentation or extension logic silently treated as runtime root

---

## 6. Final Rule

Server and runtime subtrees must remain repository-visible as the platform’s live operational surfaces.

---

## 7. Status

This document is the active canonical server/runtime subtree mapping until replaced by a stricter runtime repository map.
