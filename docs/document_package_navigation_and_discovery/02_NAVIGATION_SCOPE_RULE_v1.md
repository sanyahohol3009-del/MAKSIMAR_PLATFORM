# 02 NAVIGATION SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how package navigation should be bounded and interpreted
Rule: package navigation scope must remain explicit so discovery stays bounded, meaningful, and readable

---

## 1. Purpose

This document defines the navigation-scope rule of the platform.

It exists to preserve:
- bounded package navigation
- lower ambiguity around what discovery should cover
- continuity between package role and package entry strategy
- a stable base for later navigation hardening

---

## 2. Scope Principle

Package navigation scope should remain understandable in terms of:
- what package set is in play
- what remains outside scope for a given navigation step
- what level of navigation is primary
- how scope differs across package families

---

## 3. Required Rule

Package navigation scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined navigation boundaries
- package discovery treated as universal search by default
- navigation growth with no readable boundary
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature navigation layer first defines where to search before it relies on discovery results.

---

## 6. Status

This document is the active canonical navigation-scope rule until replaced by a stricter scope reference.
