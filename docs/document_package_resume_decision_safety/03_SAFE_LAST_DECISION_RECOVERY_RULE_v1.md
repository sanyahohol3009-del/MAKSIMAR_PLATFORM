# 03 SAFE LAST DECISION RECOVERY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for safely recovering the last meaningful decision across documentation packages
Rule: the last meaningful decision must remain safely recoverable so maintainers can resume from the right decision point without unsafe reconstruction from scattered history

---

## 1. Purpose

This document defines the safe-last-decision-recovery rule of the platform.

It exists to preserve:
- readable last-decision recovery
- lower ambiguity around where work last converged
- continuity between package history and resumed decision flow
- a stable base for later decision hardening

---

## 2. Decision Principle

Safe last-decision recovery should remain understandable in terms of:
- what was decided
- what was not decided yet
- why that decision position matters now
- how safe decision recovery preserves continuity

---

## 3. Required Rule

Safe last-decision recovery should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- last decision guessed only from recent chat memory
- decision recovery spread across too many files by default
- last-decision meaning preserved only in operator memory
- continuation that hides where the last real decision happened

---

## 5. Final Rule

A mature documentation system preserves the last meaningful decision safely before session gaps turn progress into guesswork.

---

## 6. Status

This document is the active canonical safe-last-decision-recovery rule until replaced by a stricter decision-safety reference.
