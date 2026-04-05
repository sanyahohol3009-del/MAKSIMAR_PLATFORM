# 06 REGISTRY AND SUMMARY CONFIDENCE ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping recovery confidence aligned with registry and summary layers
Rule: recovery-confidence signals must remain aligned with registry and summary surfaces so recovered package meaning does not drift away from declared metadata and summary meaning

---

## 1. Purpose

This document defines the registry-and-summary-confidence-alignment rule of the platform.

It exists to preserve:
- readable cross-layer confidence orientation
- lower ambiguity across confidence, registry, and summary layers
- continuity between recovered package meaning and declared package signals
- a stable base for later confidence hardening

---

## 2. Alignment Principle

Registry and summary confidence alignment should remain understandable in terms of:
- what confidence signals align with registry meaning
- what summary fields support confident recovery
- how alignment preserves trust
- how interpretive drift is avoided

---

## 3. Required Rule

Registry and summary confidence alignment should remain:
- explicit
- readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- confidence signals conflicting with registry or summary meaning
- silent drift between recovered confidence and machine-readable layers
- alignment guessed only from memory
- confidence claims with no cross-layer discipline

---

## 5. Final Rule

A mature documentation system keeps recovery confidence aligned with registry and summary layers because safe continuation depends on that stability.

---

## 6. Status

This document is the active canonical registry-and-summary-confidence-alignment rule until replaced by a stricter alignment reference.
