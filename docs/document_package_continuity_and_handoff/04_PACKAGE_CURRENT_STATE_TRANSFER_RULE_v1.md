# 04 PACKAGE CURRENT STATE TRANSFER RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for transferring current package state across sessions and handoff points
Rule: current package state must remain clearly transferable so package maturity and position are not re-derived from scattered files every time work resumes

---

## 1. Purpose

This document defines the package-current-state-transfer rule of the platform.

It exists to preserve:
- readable current-state transfer
- lower ambiguity around package maturity
- continuity between package now-state and next-session use
- a stable base for later continuity hardening

---

## 2. State Principle

Current state transfer should remain understandable in terms of:
- what is established now
- what is active now
- what status best describes the package
- how state transfer preserves continuity

---

## 3. Required Rule

Current state transfer should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- package current state guessed only from recent chat memory
- state transfer spread across too many files by default
- current-state meaning preserved only in operator memory
- handoff that hides what the package currently is

---

## 5. Final Rule

A mature documentation system transfers current package state clearly before time gaps turn active meaning into uncertainty.

---

## 6. Status

This document is the active canonical package-current-state-transfer rule until replaced by a stricter continuity reference.
