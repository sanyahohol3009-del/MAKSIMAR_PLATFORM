# CORE INVARIANTS AND FORBIDDEN DRIFT v1

Status: active canonical core invariant rule
Scope: platform-level architecture invariants and unacceptable drift
Rule: core architectural invariants must remain visible so drift can be detected before the platform loses coherence

---

## 1. Purpose

This document defines major core invariants and forbidden drift patterns.

It exists to prevent:
- silent architectural decay
- convenience shortcuts that break long-term structure
- accidental platform incoherence

---

## 2. Core Invariants

The platform should preserve invariants such as:
- modular rather than flat growth
- explicit layer boundaries
- explicit truth sources
- no silent dashboard truth ownership
- no silent control/execution collapse
- no uncontrolled dependency on one optional hardware extension
- no abandonment of full-platform validation discipline
- documentation remains part of the system

---

## 3. Forbidden Drift Examples

The following types of drift are forbidden:
- presentation layer redefining truth
- UI or shell becoming the hidden backend authority
- optional extension becoming required legitimacy
- new domains appearing with no documentation
- whole-platform validation disappearing in favor of partial checks only
- policy and compute collapsing into one blob

---

## 4. Required Rule

When a new change is proposed, it should be evaluated not only for correctness,
but also for architectural drift risk against these invariants.

---

## 5. Final Rule

A platform remains coherent because its invariants stay visible and defended.

---

## 6. Status

This document is the active canonical invariant and forbidden drift rule until replaced by a stricter architecture hardening reference.
