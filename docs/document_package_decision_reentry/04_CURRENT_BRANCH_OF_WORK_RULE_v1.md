# 04 CURRENT BRANCH OF WORK RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for preserving the current branch of work across sessions and handoff points
Rule: the current branch of work must remain readable so maintainers can resume on the right path instead of re-deriving which workstream is active

---

## 1. Purpose

This document defines the current-branch-of-work rule of the platform.

It exists to preserve:
- readable workstream recovery
- lower ambiguity around which line of work is active
- continuity between package state and package continuation path
- a stable base for later reentry hardening

---

## 2. Branch Principle

Current branch of work should remain understandable in terms of:
- what workstream is active now
- what alternatives are not primary now
- what branch matters most at reentry
- how branch recovery preserves continuity

---

## 3. Required Rule

Current branch of work should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- current branch guessed only from recent memory
- branch recovery spread across too many artifacts by default
- branch meaning preserved only in operator memory
- reentry that hides which work path is actually active

---

## 5. Final Rule

A mature documentation system preserves the current branch of work clearly before time gaps turn active direction into uncertainty.

---

## 6. Status

This document is the active canonical current-branch-of-work rule until replaced by a stricter reentry reference.
