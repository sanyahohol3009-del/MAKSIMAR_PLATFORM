# 02 PACKAGE APPLICABILITY SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how package applicability should be interpreted across documentation layers
Rule: package applicability scope must remain explicit so package use stays bounded, readable, and justified

---

## 1. Purpose

This document defines the package-applicability-scope rule of the platform.

It exists to preserve:
- bounded package use
- lower ambiguity around applicability
- continuity between package role and package usage
- a stable base for later applicability hardening

---

## 2. Scope Principle

Package applicability scope should remain understandable in terms of:
- what the package currently applies to
- what remains outside its justified use
- what package family it belongs to
- how applicability differs across package states

---

## 3. Required Rule

Package applicability scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined package applicability
- packages treated as universally applicable by default
- applicability growth with no readable boundary
- applicability ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature applicability layer first defines where a package should be used before it relies on that package.

---

## 6. Status

This document is the active canonical package-applicability-scope rule until replaced by a stricter scope reference.
