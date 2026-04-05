# 06 SUMMARY REGISTRY COMPATIBILITY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping structured package summaries compatible with the central document registry
Rule: package summaries must remain registry-compatible so package orientation can flow into registry-backed navigation without silent translation drift

---

## 1. Purpose

This document defines the summary-registry-compatibility rule of the platform.

It exists to preserve:
- readable package-to-registry continuity
- lower ambiguity across summary and registry layers
- continuity between package overview and machine-readable navigation
- a stable base for later compatibility hardening

---

## 2. Compatibility Principle

Summary registry compatibility should remain understandable in terms of:
- what summary fields align with registry fields
- what values remain interoperable
- what compatibility preserves navigation trust
- how translation drift is avoided

---

## 3. Required Rule

Summary registry compatibility should remain:
- explicit
- machine-readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- summaries that conflict with registry meaning
- silent translation assumptions
- compatibility guessed only from memory
- summary structure that cannot map cleanly into registry interpretation

---

## 5. Final Rule

A mature documentation system keeps package summaries compatible with the registry because orientation depends on that continuity.

---

## 6. Status

This document is the active canonical summary-registry-compatibility rule until replaced by a stricter compatibility reference.
