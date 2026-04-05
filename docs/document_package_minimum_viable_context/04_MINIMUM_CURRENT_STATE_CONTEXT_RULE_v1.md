# 04 MINIMUM CURRENT STATE CONTEXT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for preserving minimum current package state context across sessions and handoff points
Rule: minimum current-state context must remain readable so maintainers can recover what is true now without reconstructing state from scattered artifacts

---

## 1. Purpose

This document defines the minimum-current-state-context rule of the platform.

It exists to preserve:
- readable current-state recovery
- lower ambiguity around package maturity
- continuity between package now-state and resumed work
- a stable base for later context hardening

---

## 2. State Principle

Minimum current-state context should remain understandable in terms of:
- what is established now
- what is active now
- what status best describes the package
- how state context preserves continuity

---

## 3. Required Rule

Minimum current-state context should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- current package state guessed only from recent memory
- state context spread across too many files by default
- current-state meaning preserved only in operator memory
- context that hides what the package currently is

---

## 5. Final Rule

A mature documentation system preserves current-state context clearly before time gaps turn active meaning into uncertainty.

---

## 6. Status

This document is the active canonical minimum-current-state-context rule until replaced by a stricter context reference.
