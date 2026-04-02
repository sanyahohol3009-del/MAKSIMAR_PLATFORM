# AUTOMATED CHECKS AND TRIGGERS v1

Status: active canonical trigger rule
Scope: when and why validation should run
Rule: automated checks must be triggered intentionally by change, schedule, or risk event

---

## 1. Purpose

This document defines canonical triggers for automated checks.

It exists to prevent:
- random validation timing
- missed checks after important changes
- over-triggering expensive validation without reason
- under-triggering whole-platform integrity checks

---

## 2. Canonical Trigger Types

Checks may be triggered by:
- file changes
- code commits
- pre-push events
- merge/release preparation
- scheduled validation
- runtime anomaly detection
- future post-update verification

---

## 2.1 Periodic Full Platform Trigger

In addition to change-based triggers, the system must support periodic full-platform validation.

Examples:
- nightly full suite
- scheduled weekly full suite
- scheduled parallel full suite

This periodic trigger is mandatory because not all regressions are visible through change-local checks.

---

## 3. Required Rule

Triggers must be:
- documented
- predictable
- bounded
- tier-aware

A trigger should be explainable in terms of:
- what changed
- what risk exists
- what validation tier is appropriate
- whether whole-platform integrity must be rechecked

---

## 4. Trigger Examples

Examples include:
- changed file in core contract area → fast + layer tests
- release candidate → full suite
- nightly schedule → full + deep validation
- periodic schedule → full-platform suite
- repeated runtime anomaly → health verification pass

---

## 5. Trigger Escalation Principle

Not every event requires the same validation depth.

However:
- risky changes may escalate to deeper tiers
- scheduled integrity checks must still occur even without risky visible changes
- full-platform checks must not disappear just because change-local checks are green

---

## 6. What Is Forbidden

The following remain forbidden:
- validation with no known trigger logic
- always running maximum-cost validation on every tiny change
- no validation after risky change classes
- no recurring whole-platform validation schedule
- silent drift because scheduled checks were never formalized

---

## 7. Final Rule

Checks should run for a reason.
That reason should be explainable.
Whole-platform validation should also run periodically even without a single dramatic trigger event.

---

## 8. Status

This document is the active canonical trigger rule until replaced by a stricter validation automation standard.
