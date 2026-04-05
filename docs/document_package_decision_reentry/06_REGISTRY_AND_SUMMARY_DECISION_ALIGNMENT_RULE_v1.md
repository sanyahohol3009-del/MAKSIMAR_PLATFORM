# 06 REGISTRY AND SUMMARY DECISION ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package decision reentry aligned with registry and summary layers
Rule: package decision-reentry signals must remain aligned with registry and summary surfaces so recovered decision meaning does not drift away from declared metadata and summary meaning

---

## 1. Purpose

This document defines the registry-and-summary-decision-alignment rule of the platform.

It exists to preserve:
- readable cross-layer decision orientation
- lower ambiguity across reentry, registry, and summary layers
- continuity between recovered decision meaning and declared package signals
- a stable base for later reentry hardening

---

## 2. Alignment Principle

Registry and summary decision alignment should remain understandable in terms of:
- what decision signals align with registry meaning
- what summary fields support decision reentry
- how alignment preserves trust
- how interpretive drift is avoided

---

## 3. Required Rule

Registry and summary decision alignment should remain:
- explicit
- readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- decision-reentry signals conflicting with registry or summary meaning
- silent drift between recovered decision context and machine-readable layers
- alignment guessed only from memory
- decision-reentry claims with no cross-layer discipline

---

## 5. Final Rule

A mature documentation system keeps decision reentry aligned with registry and summary layers because safe continuation depends on that stability.

---

## 6. Status

This document is the active canonical registry-and-summary-decision-alignment rule until replaced by a stricter alignment reference.
