# 02 CONTEXT SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how minimum viable context should be bounded and interpreted across documentation packages
Rule: minimum viable context scope must remain explicit so package context stays bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the context-scope rule of the platform.

It exists to preserve:
- bounded context interpretation
- lower ambiguity around what minimum context must include
- continuity between package role and package recovery
- a stable base for later context hardening

---

## 2. Scope Principle

Minimum viable context scope should remain understandable in terms of:
- what package signals must survive first
- what remains outside minimum context
- what context level is primary
- how scope differs across package families

---

## 3. Required Rule

Minimum viable context scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined context boundaries
- minimum context treated as full package replay
- context growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature context layer first defines what must survive a handoff before it relies on context quality.

---

## 6. Status

This document is the active canonical context-scope rule until replaced by a stricter scope reference.
