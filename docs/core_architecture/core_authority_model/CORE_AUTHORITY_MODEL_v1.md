# CORE AUTHORITY MODEL v1

Status: active canonical authority model
Scope: high-level authority structure across the core platform
Rule: authority must remain explicit so truth, control, execution, observation, and presentation do not silently assume each other’s roles

---

## 1. Purpose

This document defines the high-level authority model of the platform.

It exists to preserve clarity about:
- who defines rules
- who executes
- who observes
- who presents
- who must not overstep

---

## 2. Authority Principle

Authority in the platform is layered, not flat.

Different layers may have authority over different things, such as:
- rules and invariants
- governance and constraints
- runtime execution
- validation and classification
- downstream presentation

These are not the same authority.

---

## 3. Canonical Authority Orientation

The preferred orientation is:

- canonical contracts and governance define what is allowed
- runtime/execution acts within allowed boundaries
- observability interprets runtime/system condition
- dashboard/presentation exposes downstream views
- extensions attach through explicit interfaces

---

## 4. Required Rule

A layer may perform only the type of authority appropriate to its role.

Presentation must not become execution authority.
Diagnostics must not become truth authority.
Optional extensions must not become legitimacy authority.

---

## 5. Final Rule

A coherent system requires explicit authority boundaries.

---

## 6. Status

This document is the active canonical authority model until replaced by a stricter authority architecture reference.
