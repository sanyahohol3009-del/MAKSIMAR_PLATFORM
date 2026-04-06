# 03 REPO ROOT GUARD CONTRACT v1

Status: active canonical repo-root-guard contract
Scope: design contract for future repo-root validation before test execution
Rule: repo-root guard behavior must remain explicit so full-suite validation is not trusted from the wrong location

---

## 1. Purpose

This document defines the repo-root-guard contract of the platform.

It exists to preserve:
- readable root-check intent
- explicit wrong-root rejection semantics
- continuity between docs and future guard code
- a stable base for later repo-root guard implementation

---

## 2. Contract Principle

Repo-root guard design should remain understandable in terms of:
- what path is expected
- what marker or condition proves correct root
- what rejection should occur if root is wrong
- what operator guidance should be shown next

---

## 3. Required Rule

Repo-root guard design should remain:
- explicit
- lightweight
- deterministic
- diagnosable
- compatible with canonical validation entry rules

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting full-suite validation from arbitrary directories
- silent acceptance of wrong-root execution
- hidden root assumptions in implementation
- weak operator feedback on root failure

---

## 5. Final Rule

A mature validation guard checks location before it checks code.

---

## 6. Status

This document is the active canonical repo-root-guard contract until replaced by a stricter repo-root verification reference.
