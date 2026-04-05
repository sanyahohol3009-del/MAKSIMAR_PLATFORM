# 03 SYNC DIRECTION MODEL v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: direction model for how package and registry layers inform synchronization
Rule: sync direction must remain explicit so package/registry alignment does not collapse into circular ambiguity

---

## 1. Purpose

This document defines the sync-direction model of the platform.

It exists to preserve:
- readable synchronization direction
- lower ambiguity around authority flow
- continuity between canonical package meaning and registry meaning
- a stable base for later sync hardening

---

## 2. Direction Principle

Sync direction should remain understandable in terms of:
- what originates in package meaning
- what originates in registry representation
- what alignment is mirrored
- what should not be inferred circularly

---

## 3. Required Rule

Sync direction should remain:
- explicit
- authority-aware
- machine-readable
- non-circular
- stable

---

## 4. What Is Forbidden

The following remain forbidden:
- circular sync logic with no authority boundary
- package and registry layers redefining each other blindly
- sync direction guessed only from habit
- hidden precedence rules

---

## 5. Final Rule

A mature sync layer knows which side explains and which side reflects.

---

## 6. Status

This document is the active canonical sync-direction model until replaced by a stricter sync-direction reference.
