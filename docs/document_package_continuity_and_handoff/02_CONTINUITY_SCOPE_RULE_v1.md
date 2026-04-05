# 02 CONTINUITY SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how package continuity and handoff should be bounded and interpreted
Rule: continuity scope must remain explicit so package handoff stays bounded, meaningful, and readable

---

## 1. Purpose

This document defines the continuity-scope rule of the platform.

It exists to preserve:
- bounded continuity interpretation
- lower ambiguity around what a handoff should include
- continuity between package role and package transfer
- a stable base for later continuity hardening

---

## 2. Scope Principle

Package continuity scope should remain understandable in terms of:
- what package state must be carried forward
- what may remain outside a minimal handoff
- what continuity level is primary
- how scope differs across package families

---

## 3. Required Rule

Package continuity scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined handoff boundaries
- package continuity treated as full re-reading by default
- continuity growth with no readable boundary
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature continuity layer first defines what must survive a handoff before it relies on handoff quality.

---

## 6. Status

This document is the active canonical continuity-scope rule until replaced by a stricter scope reference.
