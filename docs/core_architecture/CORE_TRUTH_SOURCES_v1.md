# CORE TRUTH SOURCES v1

Status: active canonical truth-source rule
Scope: source-of-truth understanding across core platform layers
Rule: the project must preserve explicit truth sources and must not allow downstream interpretation layers to silently replace them

---

## 1. Purpose

This document defines the current truth-source principle for the core platform.

It exists to prevent:
- presentation becoming truth
- logs becoming the only truth by accident
- diagnostics overriding source state
- architectural ambiguity about what is authoritative

---

## 2. Truth Principle

Truth must be explicit and source-backed.

Possible truth-source families include:
- canonical contracts and models
- runtime state artifacts
- guarded lifecycle artifacts
- process/session truth
- health/incident artifacts
- repository code and tests

---

## 3. Downstream Interpretation Principle

Observability, diagnostics, and dashboards may:
- read truth
- summarize truth
- classify truth
- visualize truth

They may not:
- silently redefine truth
- invent replacement truth
- override source-backed state without explicit rule

---

## 4. Required Rule

Whenever a status or conclusion is shown,
the system should remain explainable in terms of upstream truth sources.

---

## 5. What Is Forbidden

The following remain forbidden:
- UI as source of truth
- summary as source of truth
- convenience interpretation replacing canonical state
- truth ambiguity in critical layers

---

## 6. Final Rule

Truth must stay upstream, explicit, and explainable.

---

## 7. Status

This document is the active canonical truth-source rule until replaced by a stricter truth ownership specification.
