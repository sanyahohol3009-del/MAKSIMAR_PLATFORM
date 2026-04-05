# 02 OPERATOR RESUME SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how operator-facing resume contracts should be bounded across documentation packages
Rule: operator-resume scope must remain explicit so continuation signals stay bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the operator-resume-scope rule of the platform.

It exists to preserve:
- bounded operator resume interpretation
- lower ambiguity around what must be exposed first
- continuity between package role and resume handling
- a stable base for later contract hardening

---

## 2. Scope Principle

Operator resume scope should remain understandable in terms of:
- what signals belong in early operator reentry
- what may remain outside the first resume layer
- what scope level is primary
- how scope differs across package families

---

## 3. Required Rule

Operator resume scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined operator-resume boundaries
- operator-resume treated as full package replay
- scope growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature resume layer first defines what operators must see early before it relies on resume quality.

---

## 6. Status

This document is the active canonical operator-resume-scope rule until replaced by a stricter scope reference.
