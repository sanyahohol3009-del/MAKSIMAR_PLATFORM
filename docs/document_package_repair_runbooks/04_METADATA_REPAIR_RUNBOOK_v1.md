# 04 METADATA REPAIR RUNBOOK v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: runbook for repairing package metadata issues
Rule: package metadata issues should be repaired through a readable sequence so machine-readable package meaning remains trustworthy

---

## 1. Purpose

This document defines the metadata-repair runbook of the platform.

It exists to preserve:
- readable metadata correction
- lower risk of hidden field contradiction
- continuity between package meaning and machine-readable fields
- a stable base for later metadata hardening

---

## 2. Repair Principle

Metadata repair should remain understandable in terms of:
- what field is wrong
- what field drifted
- what should be corrected first
- how repair restores internal consistency

---

## 3. Required Rule

Metadata repair should remain:
- explicit
- internally consistent
- machine-readable
- non-contradictory
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- field contradiction left unresolved
- metadata repair reduced to cosmetic editing
- path, status, or authority mismatch ignored
- machine-readable inconsistency normalized as acceptable

---

## 5. Final Rule

A mature documentation system repairs metadata as part of package trust, not after it.

---

## 6. Status

This document is the active canonical metadata-repair runbook until replaced by a stricter metadata repair reference.
