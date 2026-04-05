# 05 SYNC CONFLICT INTERPRETATION RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: interpretation rule for conflicts between package-manifest and registry metadata
Rule: sync conflicts must remain interpretable so package/registry mismatch is resolved by readable rules rather than ad hoc guessing

---

## 1. Purpose

This document defines the sync-conflict-interpretation rule of the platform.

It exists to preserve:
- readable conflict meaning
- lower ambiguity during mismatch handling
- continuity between sync policy and resolution thinking
- a stable base for later conflict hardening

---

## 2. Conflict Principle

Sync conflict interpretation should remain understandable in terms of:
- what field conflicts
- what layer currently leads
- whether the conflict is structural or minor
- what followup should restore alignment

---

## 3. Required Rule

Conflict interpretation should remain:
- explicit
- authority-aware
- field-aware
- readable
- non-improvised

---

## 4. What Is Forbidden

The following remain forbidden:
- conflict resolution by convenience only
- unreadable precedence rules
- conflicting machine-readable meanings left unresolved forever
- panic-driven metadata rewriting

---

## 5. Final Rule

A mature sync layer resolves conflict by interpretation rules, not by whichever edit happened last.

---

## 6. Status

This document is the active canonical sync-conflict-interpretation rule until replaced by a stricter sync-conflict reference.
