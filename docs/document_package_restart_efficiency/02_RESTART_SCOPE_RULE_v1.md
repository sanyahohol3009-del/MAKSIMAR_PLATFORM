# 02 RESTART SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how restart efficiency should be bounded and interpreted across documentation packages
Rule: restart scope must remain explicit so package restart stays bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the restart-scope rule of the platform.

It exists to preserve:
- bounded restart interpretation
- lower ambiguity around what restart signals should cover
- continuity between package role and resumed work
- a stable base for later restart hardening

---

## 2. Scope Principle

Restart scope should remain understandable in terms of:
- what package signals must be recoverable first
- what remains outside fast reentry scope
- what restart level is primary
- how scope differs across package families

---

## 3. Required Rule

Restart scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined restart boundaries
- restart treated as full package rereading by default
- restart growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature restart layer first defines what must be quickly recoverable before it relies on restart quality.

---

## 6. Status

This document is the active canonical restart-scope rule until replaced by a stricter scope reference.
