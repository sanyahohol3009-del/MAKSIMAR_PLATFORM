# 03 LAST DECISION RECOVERY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for recovering the last meaningful decision position across documentation packages
Rule: the last meaningful decision must remain recoverable so maintainers can resume from the right decision point without scanning the full package history

---

## 1. Purpose

This document defines the last-decision-recovery rule of the platform.

It exists to preserve:
- readable last-decision recovery
- lower ambiguity around where work last converged
- continuity between package history and resumed decision flow
- a stable base for later reentry hardening

---

## 2. Decision Principle

Last decision recovery should remain understandable in terms of:
- what was decided
- what was not decided yet
- why that decision position matters now
- how decision recovery preserves continuity

---

## 3. Required Rule

Last decision recovery should remain:
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
- package continuation that hides where the last real decision happened

---

## 5. Final Rule

A mature documentation system preserves the last meaningful decision clearly before session gaps turn progress into guesswork.

---

## 6. Status

This document is the active canonical last-decision-recovery rule until replaced by a stricter reentry reference.
