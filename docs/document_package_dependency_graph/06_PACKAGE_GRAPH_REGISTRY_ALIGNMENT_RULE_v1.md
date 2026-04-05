# 06 PACKAGE GRAPH REGISTRY ALIGNMENT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for aligning package dependency-graph meaning with the central document registry
Rule: package graph relations must remain registry-aware so upstream and downstream meaning do not drift apart across layers

---

## 1. Purpose

This document defines the package-graph-registry-alignment rule of the platform.

It exists to preserve:
- readable cross-layer graph maintenance
- lower risk of package/registry contradiction
- continuity between graph interpretation and registry updates
- a stable base for later sync hardening

---

## 2. Alignment Principle

Package graph registry alignment should remain understandable in terms of:
- what dependency or usage field changed
- whether the registry must also change
- how upstream and downstream relations stay aligned
- how alignment preserves trust

---

## 3. Required Rule

Package graph registry alignment should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- graph change with silent registry drift
- cross-layer contradiction treated as harmless
- alignment guessed only from memory
- graph trust claims with no registry discipline during maintenance

---

## 5. Final Rule

A mature documentation system keeps graph alignment inside package maintenance, not outside it.

---

## 6. Status

This document is the active canonical package-graph-registry-alignment rule until replaced by a stricter alignment reference.
