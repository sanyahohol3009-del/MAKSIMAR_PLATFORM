# OPERATOR PROCEDURE MODEL v1

Status: active canonical operator procedure model
Scope: high-level model for operator-facing runtime procedures
Rule: operator procedures must remain explicit, bounded, and explainable rather than ritualized guesswork

---

## 1. Purpose

This document defines the current operator procedure model of the platform.

It exists to preserve clarity about:
- what kinds of procedures operators need
- what those procedures are for
- why operator interaction with runtime must remain structured

---

## 2. Procedure Categories

The platform should eventually preserve operator procedure families such as:
- start procedures
- stop procedures
- health inspection procedures
- test execution procedures
- degraded-mode inspection procedures
- recovery procedures
- incident-follow-up procedures

---

## 3. Required Rule

An operator procedure should be:
- intentional
- explainable
- bounded
- tied to system meaning
- distinguishable from improvisation

---

## 4. What Is Forbidden

The following remain forbidden:
- operator actions by folklore only
- ambiguous operational steps
- health/recovery behavior explained only informally
- runtime procedures that depend on lucky memory

---

## 5. Final Rule

Operator procedures are part of runtime legitimacy, not optional convenience notes.

---

## 6. Status

This document is the active canonical operator procedure model until replaced by a stricter operator procedure reference.
