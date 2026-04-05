# 05 PACKAGE DEPENDENCY CAPTURE DISCIPLINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: practical discipline for capturing package-level depends_on metadata during rollout
Rule: package dependency capture must remain selective and meaningful so rollout builds a readable package graph rather than decorative noise

---

## 1. Purpose

This document defines the package-dependency-capture discipline of the platform.

It exists to preserve:
- useful upstream package references
- lower dependency ambiguity
- gradual growth of readable package graph structure
- a stable base for later graph hardening

---

## 2. Capture Principle

Package dependency capture should remain understandable in terms of:
- what upstream package frames the current one
- what package should be read first
- what dependencies matter interpretively
- what may remain omitted for now without breaking meaning

---

## 3. Required Rule

Package dependency capture should remain:
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

A mature package graph records the most important upstream meaning first, then deepens later.

---

## 6. Status

This document is the active canonical package-dependency-capture discipline until replaced by a stricter package dependency graph reference.
