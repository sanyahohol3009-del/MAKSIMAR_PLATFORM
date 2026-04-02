# CI CD VALIDATION RULE v1

Status: active canonical CI/CD validation rule
Scope: local validation, repository validation, future pipeline validation
Rule: validation steps must be explicit, tiered, repeatable, and capable of exercising the full platform when required

---

## 1. Purpose

This document defines the canonical CI/CD validation rule.

It exists to prevent:
- random validation habits
- inconsistent quality gates
- code changes landing without verification
- undocumented release discipline
- loss of whole-platform integrity checking

---

## 2. Canonical Validation Tiers

Validation should exist across:
- local operator checks
- pre-commit or pre-push checks
- repository or CI checks
- pre-release checks
- future nightly/deep checks

---

## 2.1 Full Platform Validation Requirement

CI/CD validation must include the ability to run a full-platform validation pass.

Partial checks are useful for speed.
Full-platform checks remain mandatory for integrity.

The project must preserve at least one validation path which exercises the whole platform rather than only changed subsystems.

---

## 3. Required Principle

The same project should be valid under:
- manual local execution
- scripted local execution
- future automated CI execution

Validation behavior should be:
- named
- scriptable
- reproducible
- diagnosable
- explainable

---

## 4. Required Rule

Validation steps must be:
- explicit
- tiered
- documented
- reproducible
- diagnosable

No important validation path should depend on “tribal knowledge only.”

---

## 4.1 Periodic Integrity Rule

CI/CD discipline must support recurring full-platform validation even outside immediate release preparation.

This exists to verify platform-wide integrity over time, not only change-local correctness.

---

## 5. What Is Forbidden

The following remain forbidden:
- undocumented “magic” validation
- release by hope
- merge by intuition
- treating one green run as permanent truth
- removing whole-platform validation because smaller checks feel faster

---

## 6. Final Rule

CI/CD is not a replacement for engineering discipline.
It is the formalization of engineering discipline.
That discipline must include whole-platform validation as well as local speed-oriented checks.

---

## 7. Status

This document is the active canonical CI/CD validation rule until replaced by a stricter delivery governance standard.
