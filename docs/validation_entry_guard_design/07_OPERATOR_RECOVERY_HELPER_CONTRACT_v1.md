# 07 OPERATOR RECOVERY HELPER CONTRACT v1

Status: active canonical operator-recovery-helper contract
Scope: design contract for lightweight operator guidance attached to validation-entry failures
Rule: recovery helper behavior must remain explicit so rejection output leads toward correction rather than confusion

---

## 1. Purpose

This document defines the operator-recovery-helper contract of the platform.

It exists to preserve:
- readable next-step guidance
- bounded operator assistance
- continuity between rejection output and runbooks
- a stable base for later helper implementation

---

## 2. Contract Principle

Recovery-helper design should remain understandable in terms of:
- what immediate next check should be performed
- what fallback command may be used
- what stage-specific remediation applies
- what runbook family the operator should consult

---

## 3. Required Rule

Recovery-helper design should remain:
- explicit
- lightweight
- stage-aware
- recovery-oriented
- consistent with diagnostics and runbook documentation

---

## 4. What Is Forbidden

The following remain forbidden:
- rejection with no corrective hint
- helper output that overwhelms the operator
- helper logic that contradicts runbook semantics
- recovery guidance hidden only in implementation details

---

## 5. Final Rule

A mature validation guard not only rejects invalid entry.
It helps the operator recover from it.

---

## 6. Status

This document is the active canonical operator-recovery-helper contract until replaced by a stricter operator-guidance reference.
