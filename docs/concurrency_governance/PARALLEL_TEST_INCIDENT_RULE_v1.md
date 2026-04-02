# PARALLEL TEST INCIDENT RULE v1

Status: active canonical parallel test incident rule
Scope: failures or anomalies observed during parallel pytest execution
Rule: incidents in parallel mode must be classified before conclusions are drawn about code correctness

---

## 1. Purpose

This document defines how to interpret and handle incidents seen during parallel test execution.

It exists to prevent:
- misclassifying contention bugs as business-logic bugs
- misclassifying flaky tests as stable failures
- abandoning parallel mode without diagnosis
- trusting green serial mode too much when parallel mode reveals isolation defects

---

## 2. Core Principle

A failure in parallel mode may indicate one of several categories:

- real code defect
- test isolation defect
- shared resource collision
- worker lifecycle defect
- flaky/non-deterministic test behavior
- environment instability

Parallel failure must be classified before architectural conclusions are made.

---

## 3. Required Incident Handling Order

The preferred order is:

1. record the failing mode
2. identify whether the failure reproduces in serial mode
3. inspect for shared resources or order dependence
4. inspect for worker/process anomalies
5. classify the incident
6. choose remediation

---

## 4. Classification Guidance

### 4.1 Serial and parallel both fail
Likely:
- real code defect
- real test defect
- environment defect

### 4.2 Serial passes, parallel fails
Likely:
- isolation defect
- shared resource collision
- ordering defect
- hidden mutable state
- flaky timing issue

### 4.3 Parallel sometimes fails, sometimes passes
Likely:
- flaky parallel behavior
- non-deterministic setup
- unstable shared resource handling
- worker timing sensitivity

---

## 5. Required Fallback Rule

When parallel incidents appear:
- serial mode remains the fallback
- bounded parallel mode remains the diagnostic middle step
- auto-scaled mode should not remain the only evidence source

---

## 6. Required Future Hardening

The platform should later support:
- incident tagging for parallel-only failures
- optional quarantine list for temporarily parallel-unsafe tests
- per-worker incident traces
- parallel incident metrics
- retry classification with explicit labels

---

## 7. What Is Forbidden

The following remain forbidden:
- treating every parallel failure as a code logic failure
- treating every serial green run as proof that the suite is healthy
- silently disabling parallel mode without diagnosis
- accepting flaky behavior as normal

---

## 8. Final Rule

Parallel incidents are diagnostic signals.
They must be classified, not guessed.

---

## 9. Status

This document is the active canonical parallel test incident rule until replaced by a stricter parallel execution incident standard.
