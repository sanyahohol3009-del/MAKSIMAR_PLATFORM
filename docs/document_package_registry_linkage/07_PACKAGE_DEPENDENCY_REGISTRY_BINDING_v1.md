# 07 PACKAGE DEPENDENCY REGISTRY BINDING v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: binding rules for package dependency meaning across package-manifest and registry layers
Rule: package dependency metadata must remain aligned across package and registry layers so graph meaning remains readable

---

## 1. Purpose

This document defines the package-dependency-registry binding of the platform.

It exists to preserve:
- readable upstream package relations
- lower graph ambiguity
- continuity between package manifests and registry metadata
- a stable base for later graph hardening

---

## 2. Binding Principle

Package-dependency binding should remain understandable in terms of:
- what upstream package matters
- what prior package should be read first
- how dependency meaning appears in both layers
- how dependency metadata remains selective and useful

---

## 3. Required Rule

Package-dependency binding should remain:
- explicit
- selective
- meaningful
- machine-readable
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- package dependencies expressed in one layer but absent in the other forever
- random graph growth
- decorative dependency metadata
- unreadable dependency sprawl

---

## 5. Final Rule

A mature documentation graph keeps upstream meaning aligned across its layers.

---

## 6. Status

This document is the active canonical package-dependency-registry binding until replaced by a stricter dependency binding reference.
