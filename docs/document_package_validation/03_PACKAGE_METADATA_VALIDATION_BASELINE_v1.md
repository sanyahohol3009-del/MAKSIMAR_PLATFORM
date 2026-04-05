# 03 PACKAGE METADATA VALIDATION BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline validation rules for package metadata
Rule: package metadata should be validation-aware so machine-readable package meaning remains trustworthy

---

## 1. Purpose

This document defines the package-metadata-validation baseline of the platform.

It exists to preserve:
- readable metadata checking
- lower risk of field contradiction
- continuity between package meaning and machine-readable fields
- a stable base for later metadata hardening

---

## 2. Metadata Principle

Package-metadata validation should remain understandable in terms of:
- id consistency
- title readability
- path correctness
- status meaning
- authority meaning
- dependency and used_by field validity

---

## 3. Required Rule

Package-metadata validation should remain:
- explicit
- internally consistent
- machine-readable
- non-contradictory
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- conflicting metadata fields treated as harmless
- metadata validation reduced to decoration
- path, status, or authority mismatch ignored indefinitely
- machine-readable contradiction normalized as acceptable

---

## 5. Final Rule

A mature documentation system validates metadata as part of package trust, not after it.

---

## 6. Status

This document is the active canonical package-metadata-validation baseline until replaced by a stricter metadata validation reference.
