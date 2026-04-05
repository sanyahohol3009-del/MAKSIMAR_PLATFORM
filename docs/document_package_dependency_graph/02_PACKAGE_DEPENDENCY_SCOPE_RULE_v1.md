# 02 PACKAGE DEPENDENCY SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how package dependencies should be interpreted across documentation layers
Rule: package dependency scope must remain explicit so package relations stay bounded, meaningful, and readable

---

## 1. Purpose

This document defines the package-dependency-scope rule of the platform.

It exists to preserve:
- bounded dependency interpretation
- lower ambiguity around what package relations actually mean
- continuity between package role and package dependency
- a stable base for later graph hardening

---

## 2. Scope Principle

Package dependency scope should remain understandable in terms of:
- what upstream package frames the current one
- what downstream package may rely on it
- what remains outside the dependency relation
- how dependency differs across package families

---

## 3. Required Rule

Package dependency scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined dependency meaning
- packages treated as related without readable justification
- dependency growth with no boundary discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature graph layer first defines what a dependency relation means before it relies on that relation.

---

## 6. Status

This document is the active canonical package-dependency-scope rule until replaced by a stricter scope reference.
