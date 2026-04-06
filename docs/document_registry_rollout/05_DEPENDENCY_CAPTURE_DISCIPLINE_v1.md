# 05 DEPENDENCY CAPTURE DISCIPLINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: practical discipline for capturing depends_on metadata during registry rollout
Rule: dependency capture must remain selective and meaningful so rollout builds a readable graph rather than decorative noise

---

## 1. Purpose

This document defines the dependency-capture discipline of the platform.

It exists to preserve:
- useful upstream references
- lower dependency ambiguity
- gradual growth of readable graph structure
- a stable base for later graph hardening

---

## 2. Capture Principle

Dependency capture should remain understandable in terms of:
- what upstream package or document frames the current one
- what law or baseline should be read first
- what dependencies matter interpretively
- what dependencies may remain omitted for now without breaking meaning

---

## 3. Required Rule

Dependency capture should remain:
- explicit
- selective
- meaningful
- incremental
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- empty dependency thinking forever
- fake completeness through giant random dependency lists
- dependency metadata added only for decoration
- overloading rollout with graph perfectionism

---

## 5. Final Rule

A mature registry records the most important upstream meaning first, then deepens later.

---

## 6. Status

This document is the active canonical dependency-capture discipline until replaced by a stricter dependency graph reference.
