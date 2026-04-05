# 02 DECISION REENTRY SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how decision reentry should be bounded and interpreted across documentation packages
Rule: decision reentry scope must remain explicit so package decision recovery stays bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the decision-reentry-scope rule of the platform.

It exists to preserve:
- bounded decision recovery
- lower ambiguity around what decision signals must survive
- continuity between package role and decision continuation
- a stable base for later reentry hardening

---

## 2. Scope Principle

Decision reentry scope should remain understandable in terms of:
- what decision signals must be recoverable first
- what remains outside minimum reentry scope
- what reentry level is primary
- how scope differs across package families

---

## 3. Required Rule

Decision reentry scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined decision-reentry boundaries
- decision reentry treated as full package replay
- reentry growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature reentry layer first defines what decision context must survive before it relies on reentry quality.

---

## 6. Status

This document is the active canonical decision-reentry-scope rule until replaced by a stricter scope reference.
