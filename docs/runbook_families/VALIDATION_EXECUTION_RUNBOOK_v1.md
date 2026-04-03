# VALIDATION EXECUTION RUNBOOK v1

Status: active canonical validation-execution runbook
Scope: operator-facing validation execution procedure
Rule: validation execution must remain structured enough that fast checks, full checks, serial fallback, and parallel execution are used intentionally

---

## 1. Purpose

This document defines the canonical validation execution runbook of the platform.

It exists to preserve:
- disciplined validation execution
- distinction between validation tiers
- full-platform integrity checking in practice
- continuity between validation policy and operator behavior

---

## 2. Validation Execution Intent

Validation execution should help the operator determine:
- what validation scope is appropriate
- when full-platform validation is required
- when serial fallback matters
- how to interpret validation mode as part of engineering discipline

---

## 3. Canonical Validation Execution Procedure

The operator should conceptually follow this order:

1. determine whether the situation calls for fast, focused, or full-platform validation
2. preserve serial fallback as correctness discipline
3. use bounded or hardware-scaled parallel validation where appropriate
4. interpret results in context rather than by color alone
5. preserve whole-platform validation rhythm even when local checks are green

---

## 4. Required Rule

Validation execution should remain:
- explicit
- repeatable
- tier-aware
- scope-aware
- tied to platform integrity discipline

---

## 5. What Is Forbidden

The following remain forbidden:
- validation by whim only
- trusting partial checks forever
- abandoning serial fallback discipline
- treating full-platform validation as optional forever

---

## 6. Final Rule

A serious platform validates intentionally, not only conveniently.

---

## 7. Status

This document is the active canonical validation-execution runbook until replaced by a stricter validation runbook reference.
