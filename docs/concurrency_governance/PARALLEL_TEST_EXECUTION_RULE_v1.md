# PARALLEL TEST EXECUTION RULE v1

Status: active canonical parallel test execution rule
Scope: pytest and future test runners
Rule: tests must be written so that parallel execution is safe, observable, and optional

---

## 1. Purpose

This document defines the canonical rule for parallel test execution.

It exists to prevent:
- test suites that only pass in serial mode
- hidden shared file collisions
- shared port collisions
- non-deterministic CI behavior
- fake confidence from single-thread-only testing

---

## 2. Core Principle

The test suite must support:
- serial mode
- bounded parallel mode
- hardware-scaled parallel mode where safe

Parallel execution is an architectural quality signal, not just a speed trick.

---

## 3. Required Test Discipline

Tests must avoid:
- shared mutable files
- fixed temp paths
- shared mutable global state
- fixed ports unless isolated
- hidden order dependencies
- cross-test residue

---

## 4. Required Compatibility

Tests should be compatible with:
- `pytest`
- `pytest -n 2`
- `pytest -n auto`
- future CI parallelization

---

## 5. Fallback Rule

Serial mode must always remain available as the canonical fallback.

Parallel mode is preferred where stable.
Serial mode remains the correctness fallback.

---

## 6. What Is Forbidden

The following remain forbidden:
- assuming tests run in one process only
- session fixtures that silently own shared mutable state
- test logic dependent on execution order
- hidden filesystem collisions

---

## 7. Final Rule

A healthy test suite should pass in serial mode and parallel mode unless explicitly documented otherwise.

---

## 8. Status

This document is the active canonical parallel test execution rule until replaced by a stricter test isolation standard.
