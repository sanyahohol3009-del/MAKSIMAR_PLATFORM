# 06 REGISTRY AWARE INTERPRETATION RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package interpretation aligned with the central document registry
Rule: package interpretation must remain registry-aware so package status, authority, and lifecycle meaning do not drift apart across layers

---

## 1. Purpose

This document defines the registry-aware-interpretation rule of the platform.

It exists to preserve:
- readable cross-layer interpretation maintenance
- lower risk of package/registry contradiction
- continuity between package meaning and registry metadata
- a stable base for later sync hardening

---

## 2. Alignment Principle

Registry-aware interpretation should remain understandable in terms of:
- what interpretation field changed
- whether the registry must also change
- how status and authority stay aligned
- how alignment preserves trust

---

## 3. Required Rule

Registry-aware interpretation should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- interpretation change with silent registry drift
- cross-layer contradiction treated as harmless
- alignment guessed only from memory
- interpretation trust claims with no registry discipline during maintenance

---

## 5. Final Rule

A mature documentation system keeps interpretation alignment inside package maintenance, not outside it.

---

## 6. Status

This document is the active canonical registry-aware-interpretation rule until replaced by a stricter alignment reference.
