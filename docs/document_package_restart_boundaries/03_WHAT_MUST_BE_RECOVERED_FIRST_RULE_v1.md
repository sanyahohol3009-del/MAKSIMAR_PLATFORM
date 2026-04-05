# 03 WHAT MUST BE RECOVERED FIRST RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for what must be recovered first during package restart
Rule: the first recovery layer must remain readable so maintainers can re-enter from the right essentials before widening restart depth

---

## 1. Purpose

This document defines the what-must-be-recovered-first rule of the platform.

It exists to preserve:
- readable early recovery priorities
- lower ambiguity around essential restart signals
- continuity between package meaning and package reentry
- a stable base for later boundary hardening

---

## 2. Priority Principle

What must be recovered first should remain understandable in terms of:
- what signals are essential immediately
- what package meaning cannot be deferred
- what recovery order preserves trust
- how early recovery reduces reentry cost

---

## 3. Required Rule

First-recovery priority should remain:
- explicit
- compact
- meaningful
- readable
- non-random

---

## 4. What Is Forbidden

The following remain forbidden:
- essential restart signals guessed only from memory
- first-recovery logic spread across too many files by default
- critical restart priorities preserved only in operator memory
- reentry that starts from arbitrary details instead of essentials

---

## 5. Final Rule

A mature documentation system defines essential first recovery before it expands restart depth.

---

## 6. Status

This document is the active canonical what-must-be-recovered-first rule until replaced by a stricter priority reference.
