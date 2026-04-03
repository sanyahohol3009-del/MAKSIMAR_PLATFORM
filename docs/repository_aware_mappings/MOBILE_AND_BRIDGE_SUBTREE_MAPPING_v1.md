# MOBILE AND BRIDGE SUBTREE MAPPING v1

Status: active canonical mobile/bridge subtree mapping
Scope: repository-aware mapping for mobile app, bridge, and accelerator-oriented areas
Rule: mobile and bridge subtrees must remain structurally explainable so extension logic stays readable as bounded platform access rather than hidden platform legitimacy

---

## 1. Purpose

This document defines the current repository-aware mapping for mobile and bridge-oriented subtrees.

It exists to preserve clarity about:
- where mobile extension logic lives
- where bridge-mediated access logic lives
- how these areas differ from core, runtime, and dashboard meaning
- why extension structure must remain repository-visible

---

## 2. Mobile/Bridge Mapping Principle

Mobile and bridge-oriented areas should remain understandable in terms of:
- app-shell access surfaces
- backend abstraction boundaries
- mode and fallback handling
- optional accelerator extension
- bounded relation to platform legitimacy

These areas should not become hidden roots of system identity.

---

## 3. Mapping Intent

This mapping should help the operator or future engineer explain:
- where mobile-oriented logic lives
- where bridge responsibilities live
- how mobile and bridge layers depend on deeper platform layers without replacing them

---

## 4. Required Rule

Mobile and bridge subtree interpretation should remain:
- explicit
- extension-aware
- bounded
- distinct from core authority and runtime root logic

---

## 5. What Is Forbidden

The following remain forbidden:
- mobile areas interpreted as ad hoc glue only
- bridge logic treated as invisible plumbing with no architectural meaning
- extension layers silently treated as platform root
- accelerator-facing structure detached from documentation and governance

---

## 6. Final Rule

Mobile and bridge subtrees must remain repository-visible as structured extension surfaces, not hidden coercive roots.

---

## 7. Status

This document is the active canonical mobile/bridge subtree mapping until replaced by a stricter repository-aware mobile integration map.
