# 06 DEPENDENCY DRIFT DETECTION RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: drift-detection rule for package dependency meaning across the documentation graph
Rule: package dependencies should be drift-aware so graph meaning does not decay into random or decorative linking

---

## 1. Purpose

This document defines the dependency-drift-detection rule of the platform.

It exists to preserve:
- readable dependency deviation checking
- lower graph ambiguity
- continuity between dependency claims and actual package meaning
- a stable base for later graph hardening

---

## 2. Dependency Principle

Dependency drift detection should remain understandable in terms of:
- whether a dependency remains meaningful
- whether it remains selective
- whether it has drifted into noise or bloat
- whether it still frames package interpretation in a real way

---

## 3. Required Rule

Dependency drift detection should remain:
- explicit
- selective
- meaningful
- graph-aware
- machine-readable

---

## 4. What Is Forbidden

The following remain forbidden:
- random dependency accumulation treated as harmless drift
- dependency fields drifting into appearance-only metadata
- oversized dependency lists accepted without interpretation
- graph claims with no interpretive value

---

## 5. Final Rule

A mature documentation graph detects dependency drift before graph density weakens trust.

---

## 6. Status

This document is the active canonical dependency-drift-detection rule until replaced by a stricter dependency drift reference.
