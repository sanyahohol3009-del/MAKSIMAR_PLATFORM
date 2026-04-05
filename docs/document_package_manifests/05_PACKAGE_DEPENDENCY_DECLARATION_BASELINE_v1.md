# 05 PACKAGE DEPENDENCY DECLARATION BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline rules for package-level dependency declaration in manifests
Rule: package dependencies must remain explicit so the documentation universe becomes graph-readable rather than folder-fragmented

---

## 1. Purpose

This document defines the package-dependency-declaration baseline of the platform.

It exists to preserve:
- readable upstream package relations
- lower ambiguity across package interpretation
- future graph hardening
- a stable base for machine-readable package navigation

---

## 2. Dependency Principle

Package dependency declaration should remain understandable in terms of:
- what upstream package frames the current package
- what prior law or contract should be read first
- what dependency is interpretively important
- what may remain omitted temporarily without breaking readability

---

## 3. Required Rule

Package dependency declaration should remain:
- explicit
- selective
- meaningful
- non-bloated
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- packages with no readable upstream meaning
- random dependency accumulation
- dependency metadata written only for appearance
- fake completeness through oversized dependency lists

---

## 5. Final Rule

A mature documentation graph records what a package stands on before asking others to stand on it.

---

## 6. Status

This document is the active canonical package-dependency-declaration baseline until replaced by a stricter package dependency reference.
