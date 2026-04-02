# VALIDATION TRIGGER AND SCHEDULE MODEL v1

Status: active canonical validation trigger/schedule model
Scope: when validation should run and why
Rule: validation should be triggered intentionally by change, risk, or schedule, including periodic whole-platform checks

---

## 1. Purpose

This document defines the current trigger and schedule model for validation follow-through.

It exists to preserve:
- predictable validation timing
- whole-platform integrity rhythm
- explicit reasons for validation work
- discipline against both under-checking and over-checking

---

## 2. Trigger Principle

Validation may be triggered by:
- local code change
- domain-specific change
- risky architectural change
- release preparation
- scheduled periodic whole-platform verification
- incident or anomaly follow-up

---

## 3. Schedule Principle

Not all validation should happen on the same cadence.

The project should preserve room for:
- fast local checks
- focused layer checks
- full-suite checks
- periodic whole-platform checks
- future deeper scheduled validation

---

## 4. Required Rule

The validation schedule should remain explainable in terms of:
- risk
- scope
- cost
- system integrity needs

Periodic whole-platform checking must remain part of the schedule model.

---

## 5. What Is Forbidden

The following remain forbidden:
- validation timing by pure whim
- no recurring whole-platform validation rhythm
- always running maximum-cost validation for trivial changes
- never running maximum-scope validation because it is slower

---

## 6. Final Rule

Validation should run for clear reasons, on clear rhythms, with whole-platform integrity preserved.

---

## 7. Status

This document is the active canonical validation trigger/schedule model until replaced by a stricter validation scheduling reference.
