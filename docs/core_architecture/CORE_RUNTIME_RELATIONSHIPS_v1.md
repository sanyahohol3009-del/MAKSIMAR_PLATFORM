# CORE RUNTIME RELATIONSHIPS v1

Status: active canonical runtime relationship baseline
Scope: major runtime-facing relationships in the platform
Rule: runtime relationships must remain explicit so lifecycle, supervision, execution, and observation can be understood coherently

---

## 1. Purpose

This document defines the major runtime relationships in the platform.

It exists to preserve understanding of:
- how runtime is supervised
- how guard layers relate to runtime
- how observability relates to runtime
- how presentation relates downstream to runtime truth

---

## 2. Canonical Runtime Relationship Pattern

The preferred relationship pattern is:

- runtime behavior exists
- supervision/guard layers monitor and protect it
- observability reads and interprets it
- dashboard/presentation surfaces it
- external/mobile layers consume it through explicit interfaces

---

## 3. Guard / Supervision Principle

Runtime must not be treated as isolated.
It exists in relationship with:
- supervisor logic
- heartbeat/state logic
- guard/stop-gate style protection
- diagnostics and incident interpretation

---

## 4. Required Rule

Runtime relationships must remain explicit enough that an operator or future engineer can explain:
- what is running
- who watches it
- where state is stored
- what reports on it
- what is allowed to act on it

---

## 5. Final Rule

Runtime is not only code execution.
Runtime is a relationship network that must remain explainable.

---

## 6. Status

This document is the active canonical runtime relationship baseline until replaced by a stricter runtime architecture reference.
