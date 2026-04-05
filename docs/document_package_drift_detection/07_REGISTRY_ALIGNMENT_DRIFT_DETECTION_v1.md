# 07 REGISTRY ALIGNMENT DRIFT DETECTION v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: drift-detection rule for package alignment with the central document registry
Rule: package drift detection should include registry alignment so package meaning and registry meaning remain mutually trustworthy over time

---

## 1. Purpose

This document defines the registry-alignment-drift-detection rule of the platform.

It exists to preserve:
- readable cross-layer drift detection
- lower risk of package/registry contradiction
- continuity between manifest and registry meaning
- a stable base for later sync hardening

---

## 2. Alignment Principle

Registry-alignment drift detection should remain understandable in terms of:
- identity alignment drift
- path alignment drift
- status alignment drift
- dependency alignment drift
- downstream-usage alignment drift

---

## 3. Required Rule

Registry-alignment drift detection should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- package and registry layers diverging silently
- cross-layer drift treated as harmless
- drift interpretation guessed only from memory
- package trust claims with no registry discipline

---

## 5. Final Rule

A mature documentation system detects registry-alignment drift as part of package quality, not as a separate afterthought.

---

## 6. Status

This document is the active canonical registry-alignment-drift-detection rule until replaced by a stricter alignment drift reference.
