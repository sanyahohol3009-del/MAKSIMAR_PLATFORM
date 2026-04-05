# 04 CURRENT STATE RESTART RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for recovering current package state efficiently during restart
Rule: current package state must remain restart-readable so operators can resume from what is true now instead of rediscovering state from scattered package artifacts

---

## 1. Purpose

This document defines the current-state-restart rule of the platform.

It exists to preserve:
- readable current-state recovery
- lower ambiguity around package maturity at restart time
- continuity between package now-state and resumed work
- a stable base for later restart hardening

---

## 2. State Principle

Current state restart should remain understandable in terms of:
- what is established now
- what is active now
- what state matters most at reentry
- how state recovery preserves continuity

---

## 3. Required Rule

Current state restart should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- current package state guessed only from recent memory
- state recovery spread across too many files by default
- current-state restart logic preserved only in operator memory
- restart that hides what the package currently is

---

## 5. Final Rule

A mature documentation system keeps current package state restart-readable before time gaps turn active meaning into uncertainty.

---

## 6. Status

This document is the active canonical current-state-restart rule until replaced by a stricter restart reference.
