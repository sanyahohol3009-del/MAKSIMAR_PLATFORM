# 03 MINIMUM PACKAGE IDENTITY CONTEXT RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for preserving minimum package identity context across sessions and handoff points
Rule: minimum package identity context must remain readable so maintainers can recover what the package is without scanning the full package body

---

## 1. Purpose

This document defines the minimum-package-identity-context rule of the platform.

It exists to preserve:
- readable package identity recovery
- lower ambiguity around package role
- continuity between package title and package meaning
- a stable base for later context hardening

---

## 2. Identity Principle

Minimum package identity context should remain understandable in terms of:
- what the package is for
- what layer it belongs to
- what problem it addresses
- how identity context preserves orientation

---

## 3. Required Rule

Minimum package identity context should remain:
- explicit
- compact
- meaningful
- readable
- non-decorative

---

## 4. What Is Forbidden

The following remain forbidden:
- package identity guessed only from filenames or memory
- identity context too vague to orient the reader
- package role preserved only in operator memory
- context text that obscures package identity instead of clarifying it

---

## 5. Final Rule

A mature documentation system preserves package identity context clearly before it expects deeper interpretation.

---

## 6. Status

This document is the active canonical minimum-package-identity-context rule until replaced by a stricter context reference.
