# 06 PACKAGE USAGE REGISTRY ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for aligning package applicability and usage with the central document registry
Rule: package usage must remain registry-aware so active, superseded, and historical applicability do not drift apart across layers

---

## 1. Purpose

This document defines the package-usage-registry-alignment rule of the platform.

It exists to preserve:
- readable cross-layer usage maintenance
- lower risk of package/registry contradiction
- continuity between usage interpretation and registry updates
- a stable base for later sync hardening

---

## 2. Alignment Principle

Package-usage registry alignment should remain understandable in terms of:
- what usage field changed
- whether the registry must also change
- how active, superseded, and historical applicability stay aligned
- how alignment preserves trust

---

## 3. Required Rule

Package-usage registry alignment should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- package usage change with silent registry drift
- cross-layer contradiction treated as harmless
- alignment guessed only from memory
- usage trust claims with no registry discipline during maintenance

---

## 5. Final Rule

A mature documentation system keeps usage alignment inside package maintenance, not outside it.

---

## 6. Status

This document is the active canonical package-usage-registry-alignment rule until replaced by a stricter alignment reference.
