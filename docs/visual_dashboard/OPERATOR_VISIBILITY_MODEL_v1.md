# OPERATOR VISIBILITY MODEL v1

Status: active canonical operator-visibility model
Scope: what should become visible to operators and why
Rule: operator visibility must remain structured enough that the dashboard helps understanding rather than merely emitting visual noise

---

## 1. Purpose

This document defines the current operator-visibility model of the platform.

It exists to preserve clarity about:
- what operators should be able to see
- why operator visibility matters
- how visibility differs from authority
- why visibility should remain explainable and structured

---

## 2. Visibility Principle

Operator visibility should help expose:
- runtime condition
- health or degraded state
- incident-facing meaning
- diagnostics-relevant context
- platform status and flow meaning
- future role-based or display-specific visibility where appropriate

---

## 3. Required Rule

Visibility should remain explainable in terms of:
- what upstream truth or interpretation it depends on
- what operator concern it serves
- what the visibility does not imply in terms of authority or control

---

## 4. What Is Forbidden

The following remain forbidden:
- operator visibility that looks rich but explains nothing
- dashboard visibility treated as system control authority
- visual saturation with no meaning discipline
- visibility detached from runtime, health, or diagnostics semantics

---

## 5. Final Rule

Operator visibility should support understanding, not decoration alone.

---

## 6. Status

This document is the active canonical operator-visibility model until replaced by a stricter operator visibility reference.
