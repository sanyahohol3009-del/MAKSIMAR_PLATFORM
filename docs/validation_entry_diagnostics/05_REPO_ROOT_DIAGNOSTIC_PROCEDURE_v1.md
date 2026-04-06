# 05 REPO ROOT DIAGNOSTIC PROCEDURE v1

Status: active canonical repo-root-diagnostic procedure
Scope: diagnosis of repository-root mistakes before validation launch
Rule: repository-root diagnostics must remain explicit so wrong-directory launches are quickly isolated from code-level concerns

---

## 1. Purpose

This document defines the repo-root-diagnostic procedure of the platform.

It exists to preserve:
- readable diagnosis of wrong-root launches
- lower confusion during import and collection failure
- fast elimination of directory-context mistakes
- a stable base for later guard implementation

---

## 2. Procedure Principle

Repo-root diagnosis should remain understandable in terms of:
- current working directory
- whether repository root was intended
- whether launch assumptions require repo-root visibility
- whether import behavior is consistent with current location

---

## 3. Required Rule

Repo-root diagnostics should remain:
- explicit
- quick
- foundational
- launch-aware
- suitable as the first structural check

---

## 4. What Is Forbidden

The following remain forbidden:
- skipping current-directory diagnosis
- blaming imports before checking root context
- assuming repo-root correctness without verification
- treating wrong-root launch as a mysterious Python problem

---

## 5. Final Rule

A mature validation flow checks where it is before it judges what failed.

---

## 6. Status

This document is the active canonical repo-root-diagnostic procedure until replaced by a stricter root-diagnostics reference.
