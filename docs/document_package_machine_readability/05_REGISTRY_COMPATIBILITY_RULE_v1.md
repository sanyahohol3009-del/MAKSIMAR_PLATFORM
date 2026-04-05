# 05 REGISTRY COMPATIBILITY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package machine readability compatible with the central document registry
Rule: package machine-readable structure must remain registry-compatible so package meaning can flow into registry-backed navigation without silent translation drift

---

## 1. Purpose

This document defines the registry-compatibility rule of the platform.

It exists to preserve:
- readable package-to-registry structure
- lower ambiguity across machine-readable layers
- continuity between package metadata and registry metadata
- a stable base for later compatibility hardening

---

## 2. Compatibility Principle

Registry compatibility should remain understandable in terms of:
- what package fields align with registry fields
- what values remain interoperable
- what compatibility preserves navigation trust
- how compatibility avoids translation drift

---

## 3. Required Rule

Registry compatibility should remain:
- explicit
- machine-readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- machine-readable package structure that conflicts with registry structure
- silent translation assumptions
- compatibility guessed only from memory
- package structure that cannot map cleanly into registry interpretation

---

## 5. Final Rule

A mature documentation system keeps package structure compatible with the registry because navigation depends on that continuity.

---

## 6. Status

This document is the active canonical registry-compatibility rule until replaced by a stricter compatibility reference.
