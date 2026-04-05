# 04 SAFE CURRENT BRANCH RECOVERY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for safely recovering the current branch of work across documentation packages
Rule: the current branch of work must remain safely recoverable so maintainers can resume on the right path without unsafe re-derivation of which workstream is active

---

## 1. Purpose

This document defines the safe-current-branch-recovery rule of the platform.

It exists to preserve:
- readable workstream recovery
- lower ambiguity around which line of work is active
- continuity between package state and package continuation path
- a stable base for later decision hardening

---

## 2. Branch Principle

Safe current-branch recovery should remain understandable in terms of:
- what workstream is active now
- what alternatives are not primary now
- what branch matters most at reentry
- how safe branch recovery preserves continuity

---

## 3. Required Rule

Safe current-branch recovery should remain:
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

A mature documentation system preserves the current branch of work safely before time gaps turn active direction into uncertainty.

---

## 6. Status

This document is the active canonical safe-current-branch-recovery rule until replaced by a stricter decision-safety reference.
