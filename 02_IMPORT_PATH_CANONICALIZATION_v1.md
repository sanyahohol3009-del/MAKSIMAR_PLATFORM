# 02 IMPORT PATH CANONICALIZATION v1

Status: active canonical import-path canonicalization baseline
Scope: canonical interpretation of repository import visibility during validation
Rule: import-path conditions must remain explicit so collection failures are not confused with domain logic failures

---

## 1. Purpose

This document defines the import-path canonicalization baseline of the platform.

It exists to preserve:
- readable import visibility expectations
- correct interpretation of package discovery
- explicit distinction between bootstrap failure and logic failure
- a stable base for later packaging and validation hardening

---

## 2. Import Principle

Import-path interpretation should remain understandable in terms of:
- whether repo-root visibility exists
- whether package imports succeed under the chosen entrypoint
- whether collection failure is import-related
- whether runtime code has actually been exercised yet

Import failure is not automatically business-logic failure.

---

## 3. Required Rule

Import-path discipline should remain:
- explicit
- testable
- repo-root aware
- entrypoint aware
- diagnosable

---

## 4. What Is Forbidden

The following remain forbidden:
- treating import-path failure as hundreds of independent code defects
- hiding bootstrap assumptions in operator memory only
- letting package visibility depend on luck
- using ambiguous launch modes without interpretation

---

## 5. Final Rule

A mature validation system distinguishes import visibility from actual code correctness.

---

## 6. Status

This document is the active canonical import-path canonicalization baseline until replaced by a stricter bootstrap/import reference.
