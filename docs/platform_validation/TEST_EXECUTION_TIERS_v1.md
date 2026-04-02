# TEST EXECUTION TIERS v1

Status: active canonical test tier rule
Scope: validation cost, speed, depth, and whole-platform integrity
Rule: tests must be organized into tiers so that the platform can verify itself without wasting resources unnecessarily, while preserving mandatory whole-platform validation

---

## 1. Purpose

This document defines canonical test execution tiers.

It exists to prevent:
- always running the heaviest possible validation
- no distinction between fast checks and deep checks
- wasted operator time
- poor resource discipline
- drift caused by relying only on local subsystem checks

---

## 2. Canonical Tiers

### Tier 1: Fast Checks
Examples:
- py_compile
- tiny smoke tests
- changed-layer checks

Purpose:
- protect iteration speed
- catch obvious breakage early
- keep developer feedback fast

### Tier 2: Layer Checks
Examples:
- contract family checks
- package-specific tests
- focused subsystem verification

Purpose:
- validate one bounded subsystem
- verify local architectural integrity
- avoid running the full suite for every tiny change

### Tier 3: Full Suite
Examples:
- full pytest suite
- serial or parallel depending policy

Purpose:
- validate the whole test-covered platform
- detect cross-layer regressions
- verify that subsystem changes did not damage global integrity

### Tier 4: Deep Validation
Examples:
- full suite + stress
- parallel profile validation
- future heavy diagnostics
- nightly validation

Purpose:
- detect integration drift over time
- validate platform behavior under deeper pressure
- confirm long-tail integrity beyond ordinary development rhythm

---

## 2.1 Full Platform Rule

Tier 3 and Tier 4 validation must be capable of covering the entire platform.

The project must not rely only on partial subsystem checks forever.
A full-platform validation pass remains mandatory as part of canonical engineering discipline.

---

## 2.2 Periodic Full Validation Rule

A full-platform validation run must be performed periodically even without a release event.

This exists to detect:
- cross-layer drift
- hidden integration regressions
- slow architectural inconsistency
- parallel/runtime regressions which partial checks may miss

---

## 3. Required Rule

The platform must not assume every validation event requires Tier 4.

Tier choice should reflect:
- change scope
- risk level
- release proximity
- available resources

However, Tier 3 and Tier 4 full-platform validation remain mandatory as recurring integrity checks for the whole system.

---

## 4. Resource Discipline Rule

Fast checks protect iteration speed.
Layer checks protect local correctness.
Full-suite checks protect platform integrity.
Deep checks protect long-horizon stability.

The project must preserve all of these roles and must not collapse them into one undifferentiated validation habit.

---

## 5. What Is Forbidden

The following remain forbidden:
- always running maximum-cost validation for every tiny edit
- relying forever on partial checks only
- treating one green local layer test as proof that the whole platform is healthy
- deleting full-platform validation from engineering discipline
- treating deep validation as optional forever

---

## 6. Final Rule

Fast checks protect iteration speed.
Deep checks protect system integrity.
Whole-platform checks protect architectural truth.
All are required.

---

## 7. Status

This document is the active canonical test tier rule until replaced by a stricter validation orchestration standard.
