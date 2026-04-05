# 06 SYNC UPDATE DISCIPLINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: discipline for updating package/registry sync state over time
Rule: sync updates must remain deliberate so alignment work does not create fresh ambiguity

---

## 1. Purpose

This document defines the sync-update discipline of the platform.

It exists to preserve:
- readable update order
- lower risk of chaotic sync edits
- continuity between sync policy and actual maintenance work
- a stable base for later tooling support

---

## 2. Update Principle

Sync update discipline should remain understandable in terms of:
- what changed
- what must be updated next
- how alignment is restored
- how update steps avoid contradiction

---

## 3. Required Rule

Sync update discipline should remain:
- explicit
- ordered
- machine-readable
- maintenance-aware
- non-chaotic

---

## 4. What Is Forbidden

The following remain forbidden:
- random sync edits
- updating one layer while forgetting the other indefinitely
- undocumented update order
- sync maintenance by memory only

---

## 5. Final Rule

A mature sync layer updates deliberately rather than hoping alignment will emerge by itself.

---

## 6. Status

This document is the active canonical sync-update discipline until replaced by a stricter sync-maintenance reference.
