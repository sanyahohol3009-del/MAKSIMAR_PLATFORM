# 04 SYNC METADATA MISMATCH RUNBOOK v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: runbook for repairing package/registry metadata mismatch issues
Rule: sync metadata mismatches should be repaired through a readable sequence so machine-readable cross-layer meaning remains trustworthy

---

## 1. Purpose

This document defines the sync-metadata-mismatch runbook of the platform.

It exists to preserve:
- readable metadata correction
- lower risk of hidden cross-layer contradiction
- continuity between package meaning and registry fields
- a stable base for later metadata hardening

---

## 2. Repair Principle

Sync metadata repair should remain understandable in terms of:
- what field is wrong
- what field drifted between layers
- what should be corrected first
- how repair restores internal and cross-layer consistency

---

## 3. Required Rule

Sync metadata repair should remain:
- explicit
- internally consistent
- machine-readable
- non-contradictory
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- field contradiction left unresolved across layers
- metadata repair reduced to cosmetic editing
- path, status, or authority mismatch ignored
- machine-readable inconsistency normalized as acceptable

---

## 5. Final Rule

A mature documentation system repairs sync metadata as part of documentation trust, not after it.

---

## 6. Status

This document is the active canonical sync-metadata-mismatch runbook until replaced by a stricter metadata-sync repair reference.
