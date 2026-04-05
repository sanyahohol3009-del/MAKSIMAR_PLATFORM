# 03 FAST REENTRY SIGNAL RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping fast reentry signals readable across documentation packages
Rule: package fast reentry signals must remain readable so operators can re-enter package work from the right point without scanning the full package every time

---

## 1. Purpose

This document defines the fast-reentry-signal rule of the platform.

It exists to preserve:
- readable reentry cues
- lower ambiguity around where resumed work should start
- continuity between package handling and package restart
- a stable base for later restart hardening

---

## 2. Reentry Principle

Fast reentry signals should remain understandable in terms of:
- what the package is
- what point the operator should resume from
- what signal matters first
- how reentry guidance preserves documentation trust

---

## 3. Required Rule

Fast reentry signals should remain:
- explicit
- readable
- compact
- meaningful
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- restart based only on memory or recent chat context
- reentry signals too vague to guide continuation
- reentry logic preserved only in operator memory
- package restart through random file entry by default

---

## 5. Final Rule

A mature documentation system provides fast reentry signals before session gaps turn restart into archaeology.

---

## 6. Status

This document is the active canonical fast-reentry-signal rule until replaced by a stricter restart reference.
