# 05 PARALLEL SERIAL RECOVERY RUNBOOK v1

Status: active canonical parallel-serial-recovery runbook
Scope: operator decision and recovery path when parallel and serial validation interpretation diverge
Rule: disagreement between fast and fallback validation must be handled methodically so performance does not override correctness

---

## 1. Purpose

This document defines the parallel-serial-recovery runbook of the platform.

It exists to preserve:
- explicit recovery when execution modes differ
- correctness-first interpretation
- reduced confusion around concurrency-related ambiguity
- a stable base for later validation execution hardening

---

## 2. Recovery Principle

Parallel-serial recovery should remain understandable in terms of:
- identifying disagreement between execution modes
- preserving serial fallback as a correctness reference
- interpreting parallel behavior cautiously
- deciding whether the issue is bootstrap, concurrency, or deeper logic

---

## 3. Required Rule

Parallel-serial recovery should remain:
- explicit
- correctness-first
- fallback-aware
- transition-aware
- diagnostics-readable

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting fast parallel green as final when fallback disagrees
- ignoring slower but cleaner validation evidence
- assuming disagreement is meaningless
- collapsing correctness into speed preference

---

## 5. Final Rule

A mature validation workflow uses speed aggressively but trusts correctness more.

---

## 6. Status

This document is the active canonical parallel-serial-recovery runbook until replaced by a stricter validation execution recovery reference.
