# 06 LIFECYCLE REGISTRY ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for aligning package lifecycle meaning with the central document registry
Rule: package lifecycle and supersession must remain registry-aware so active, superseded, and historical meaning do not drift apart across layers

---

## 1. Purpose

This document defines the lifecycle-registry-alignment rule of the platform.

It exists to preserve:
- readable cross-layer lifecycle maintenance
- lower risk of package/registry contradiction
- continuity between lifecycle changes and registry updates
- a stable base for later sync hardening

---

## 2. Alignment Principle

Lifecycle-registry alignment should remain understandable in terms of:
- what lifecycle field changed
- whether the registry must also change
- how active, superseded, and historical meaning stay aligned
- how alignment preserves trust

---

## 3. Required Rule

Lifecycle-registry alignment should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- lifecycle change with silent registry drift
- cross-layer contradiction treated as harmless
- alignment guessed only from memory
- lifecycle trust claims with no registry discipline during maintenance

---

## 5. Final Rule

A mature documentation system keeps lifecycle alignment inside package maintenance, not outside it.

---

## 6. Status

This document is the active canonical lifecycle-registry-alignment rule until replaced by a stricter alignment reference.
