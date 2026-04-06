# 01 VALIDATION BOOTSTRAP BASELINE v1

Status: active canonical validation-bootstrap baseline
Scope: canonical bootstrap conditions for running validation across the repository
Rule: validation must start from a known bootstrap state so collection and execution results remain trustworthy

---

## 1. Purpose

This document defines the validation-bootstrap baseline of the platform.

It exists to preserve:
- repeatable validation startup conditions
- explicit repository-root execution discipline
- stable import visibility during test collection
- a readable base for later validation automation

---

## 2. Bootstrap Principle

Validation bootstrap should remain understandable in terms of:
- correct project root
- correct Python executable
- correct pytest entrypoint
- correct import visibility
- correct environment activation

A green result without valid bootstrap is weaker than it appears.

---

## 3. Required Rule

Validation bootstrap should remain:
- explicit
- repeatable
- repo-root aware
- environment aware
- import-path aware

---

## 4. What Is Forbidden

The following remain forbidden:
- running large validation passes from arbitrary directories
- trusting collection results from broken bootstrap conditions
- mixing entrypoints with no canonical interpretation
- treating import-path failure as proof of code failure

---

## 5. Final Rule

A serious platform validates from a known bootstrap state, not from convenience.

---

## 6. Status

This document is the active canonical validation-bootstrap baseline until replaced by a stricter validation bootstrap reference.
