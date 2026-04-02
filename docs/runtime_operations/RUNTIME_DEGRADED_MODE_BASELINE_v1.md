# RUNTIME DEGRADED MODE BASELINE v1

Status: active canonical degraded-mode baseline
Scope: high-level understanding of runtime degradation
Rule: degraded mode must remain an explicit operational state, not an undocumented half-broken condition

---

## 1. Purpose

This document defines the current degraded-mode baseline of the platform.

It exists to preserve clarity about:
- what degraded mode means
- why degraded mode may happen
- how degraded mode differs from total failure
- why degraded operation is part of operational legitimacy

---

## 2. Degraded-Mode Principle

Degraded mode is not the same as normal healthy runtime,
and it is not always the same as total failure.

It may represent:
- constrained operation
- reduced capability
- protective fallback
- health-preserving or safety-preserving behavior

---

## 3. Required Rule

The platform should remain able to explain:
- why degraded mode was entered
- what capability was reduced or constrained
- what safety or continuity reason justified it
- whether recovery is possible or expected

---

## 4. What Is Forbidden

The following remain forbidden:
- degraded behavior treated as undocumented weirdness
- degraded mode with no operator-facing meaning
- collapse of runtime health language into only “green or dead”
- treating degraded mode as a meaningless embarrassment rather than controlled fallback

---

## 5. Final Rule

A mature platform recognizes degraded mode explicitly rather than pretending only perfect or broken states exist.

---

## 6. Status

This document is the active canonical degraded-mode baseline until replaced by a stricter degraded-runtime reference.
