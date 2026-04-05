# 08 PACKAGE USED BY REGISTRY BINDING v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: binding rules for downstream package usage meaning across package-manifest and registry layers
Rule: used_by metadata must remain aligned across package and registry layers so downstream interpretive meaning stays readable

---

## 1. Purpose

This document defines the package-used_by-registry binding of the platform.

It exists to preserve:
- readable downstream package relations
- lower ambiguity across future package usage
- continuity between package manifests and registry metadata
- a stable base for later graph deepening

---

## 2. Binding Principle

Package-used_by binding should remain understandable in terms of:
- what later packages may rely on the current one
- what downstream interpretive meaning exists
- how that meaning appears in both layers
- how used_by metadata remains selective and readable

---

## 3. Required Rule

Package-used_by binding should remain:
- explicit
- selective
- meaningful
- machine-readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- downstream meaning present only in one layer forever
- used_by lists grown for appearance only
- unreadable future-usage sprawl
- divergence between package and registry downstream semantics

---

## 5. Final Rule

A mature documentation graph keeps downstream meaning aligned wherever it is declared.

---

## 6. Status

This document is the active canonical package-used_by-registry binding until replaced by a stricter downstream binding reference.
