# 03 REGISTRY TO PACKAGE COVERAGE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: coverage rule from registry entries back to package reality
Rule: registry coverage should correspond to actual package structure so machine-readable indexing remains trustworthy

---

## 1. Purpose

This document defines the registry-to-package-coverage rule of the platform.

It exists to preserve:
- trustworthy registry coverage
- lower risk of phantom package entries
- continuity between indexed packages and actual package folders
- a stable base for future coverage validation

---

## 2. Coverage Principle

Registry-to-package coverage should remain understandable in terms of:
- whether a package exists in the repository
- whether its entry points to the correct path
- whether package coverage is partial or meaningful
- whether package identity is real rather than decorative

---

## 3. Required Rule

Registry-to-package coverage should remain:
- explicit
- path-aware
- reality-bound
- machine-readable
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- registry entries for non-existent package structures
- stale package references with no reality check
- decorative coverage claims
- path drift hidden behind registry growth

---

## 5. Final Rule

A mature registry indexes real package structure, not aspirational placeholders.

---

## 6. Status

This document is the active canonical registry-to-package coverage rule until replaced by a stricter coverage reference.
