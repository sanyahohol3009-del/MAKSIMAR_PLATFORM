# HEALTH INSPECTION RUNBOOK v1

Status: active canonical health inspection runbook
Scope: operator-facing health inspection procedure
Rule: runtime health must be inspected through a structured procedure rather than vague impression

---

## 1. Purpose

This document defines the canonical health inspection runbook of the platform.

It exists to preserve:
- structured health interpretation
- explicit distinction between healthy, degraded, and failed conditions
- disciplined operator inspection behavior

---

## 2. Health Inspection Intent

Health inspection should help the operator determine:
- whether runtime is healthy
- whether runtime is degraded
- whether incident-bearing conditions are visible
- whether followup is necessary

---

## 3. Canonical Health Inspection Procedure

The operator should conceptually follow this order:

1. inspect current runtime phase
2. inspect visible health-relevant signals
3. inspect whether degraded or incident meaning is present
4. distinguish stable healthy state from uncertain or abnormal state
5. decide whether continued observation, incident followup, or recovery thinking is needed

---

## 4. Required Rule

Health inspection should remain:
- explicit
- source-aware
- repeatable
- bounded
- tied to observability and runtime meaning

---

## 5. What Is Forbidden

The following remain forbidden:
- “looks okay” as the only health model
- binary thinking with no degraded-state interpretation
- operator decisions based only on emotional reaction to symptoms
- health inspection detached from runtime context

---

## 6. Final Rule

Health should be inspected deliberately, not guessed at.

---

## 7. Status

This document is the active canonical health inspection runbook until replaced by a stricter health operations reference.
