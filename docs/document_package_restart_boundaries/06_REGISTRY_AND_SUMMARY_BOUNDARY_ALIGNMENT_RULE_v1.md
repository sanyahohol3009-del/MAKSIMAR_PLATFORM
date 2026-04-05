# 06 REGISTRY AND SUMMARY BOUNDARY ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping restart boundaries aligned with registry and summary layers
Rule: restart-boundary signals must remain aligned with registry and summary surfaces so recovered package meaning does not drift away from declared metadata and summary meaning

---

## 1. Purpose

This document defines the registry-and-summary-boundary-alignment rule of the platform.

It exists to preserve:
- readable cross-layer boundary orientation
- lower ambiguity across restart framing, registry, and summary layers
- continuity between recovered package meaning and declared package signals
- a stable base for later boundary hardening

---

## 2. Alignment Principle

Registry and summary boundary alignment should remain understandable in terms of:
- what boundary signals align with registry meaning
- what summary fields support restart framing
- how alignment preserves trust
- how interpretive drift is avoided

---

## 3. Required Rule

Registry and summary boundary alignment should remain:
- explicit
- readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- boundary signals conflicting with registry or summary meaning
- silent drift between restart framing and machine-readable layers
- alignment guessed only from memory
- restart-boundary claims with no cross-layer discipline

---

## 5. Final Rule

A mature documentation system keeps restart boundaries aligned with registry and summary layers because reliable reentry depends on that stability.

---

## 6. Status

This document is the active canonical registry-and-summary-boundary-alignment rule until replaced by a stricter alignment reference.
