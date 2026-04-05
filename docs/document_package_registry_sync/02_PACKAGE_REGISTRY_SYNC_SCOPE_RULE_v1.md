# 02 PACKAGE REGISTRY SYNC SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for what package/registry metadata should participate in synchronization
Rule: sync scope must remain explicit so package-registry alignment stays readable and bounded

---

## 1. Purpose

This document defines the package-registry-sync-scope rule of the platform.

It exists to preserve:
- bounded synchronization scope
- lower ambiguity about what must align
- continuity between sync expectations and actual metadata
- a stable base for later drift detection

---

## 2. Scope Principle

Sync scope should remain understandable in terms of:
- what fields must align
- what fields may lag temporarily
- what metadata is authoritative
- what sync boundaries remain deliberate

---

## 3. Required Rule

Sync scope should remain:
- explicit
- bounded
- machine-readable
- interpretable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined sync scope
- pretending all metadata is equally sync-critical
- silent expansion of sync boundaries
- drift caused by ambiguous field ownership

---

## 5. Final Rule

A mature sync layer first defines what is in scope before trying to keep everything aligned.

---

## 6. Status

This document is the active canonical package-registry-sync-scope rule until replaced by a stricter sync-scope reference.
