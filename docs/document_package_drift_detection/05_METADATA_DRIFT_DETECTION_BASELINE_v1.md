# 05 METADATA DRIFT DETECTION BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline drift-detection rules for package metadata
Rule: package metadata should be drift-aware so machine-readable package meaning remains trustworthy over time

---

## 1. Purpose

This document defines the metadata-drift-detection baseline of the platform.

It exists to preserve:
- readable metadata deviation checking
- lower risk of hidden field drift
- continuity between package meaning and machine-readable fields
- a stable base for later metadata hardening

---

## 2. Metadata Principle

Metadata drift detection should remain understandable in terms of:
- id deviation
- title drift
- path drift
- status drift
- authority drift
- dependency and used_by field drift

---

## 3. Required Rule

Metadata drift detection should remain:
- explicit
- internally consistent
- machine-readable
- non-contradictory
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- field drift treated as harmless indefinitely
- metadata drift reduced to decoration
- path, status, or authority deviation ignored
- machine-readable drift normalized as acceptable

---

## 5. Final Rule

A mature documentation system detects metadata drift as part of package trust, not after it.

---

## 6. Status

This document is the active canonical metadata-drift-detection baseline until replaced by a stricter metadata drift reference.
