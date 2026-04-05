# 05 PACKAGE PATH REGISTRY BINDING v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: binding rules between package path meaning and registry path metadata
Rule: package paths must remain aligned across package and registry layers so navigation stays trustworthy

---

## 1. Purpose

This document defines the package-path-registry binding of the platform.

It exists to preserve:
- readable path alignment
- lower navigation ambiguity
- trustworthy machine-readable location semantics
- a stable base for future package validation

---

## 2. Binding Principle

Package-path binding should remain understandable in terms of:
- where the package actually lives
- how the registry points to it
- how path meaning remains stable
- how path drift is avoided

---

## 3. Required Rule

Package-path binding should remain:
- explicit
- path-aware
- reality-bound
- machine-readable
- stable

---

## 4. What Is Forbidden

The following remain forbidden:
- registry paths that drift from actual package folders
- path assumptions preserved only in memory
- decorative path metadata
- silent divergence between package layout and registry navigation

---

## 5. Final Rule

A mature documentation system keeps package location and registry location aligned.

---

## 6. Status

This document is the active canonical package-path-registry binding until replaced by a stricter path binding reference.
