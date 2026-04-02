# BACKEND MODE AND FALLBACK BASELINE v1

Status: active canonical backend-mode and fallback baseline
Scope: local, external, and degraded mobile execution modes
Rule: backend modes and fallback behavior must remain explicit so the platform preserves continuity across changing execution conditions

---

## 1. Purpose

This document defines the current backend-mode and fallback baseline of the platform.

It exists to preserve clarity about:
- local execution mode
- external accelerator mode
- degraded or fallback mode
- why mobile experience should survive backend changes without identity collapse

---

## 2. Backend Mode Principle

The platform should remain capable of distinguishing backend realities such as:
- local mode
- external accelerator mode
- degraded or constrained mode

These modes may differ operationally,
but should still remain unified under stable higher-level app and bridge behavior.

---

## 3. Fallback Principle

Fallback is not a shame state.
It is part of system maturity.

Fallback may preserve:
- continuity of service
- reduced but still legitimate capability
- safety under thermal, health, or attachment problems
- operator/user trust in system continuity

---

## 4. Required Rule

Backend switching or fallback behavior should remain:
- explicit
- explainable
- bounded
- non-chaotic
- non-legitimizing over core platform identity

---

## 5. What Is Forbidden

The following remain forbidden:
- backend mode confusion with no visible model
- fallback treated as undocumented weirdness
- external mode treated as the only “real” mode
- app behavior fragmented by backend-specific chaos

---

## 6. Final Rule

Backend modes may vary.
System legitimacy and operator understanding must remain stable.

---

## 7. Status

This document is the active canonical backend-mode and fallback baseline until replaced by a stricter mobile backend reference.
