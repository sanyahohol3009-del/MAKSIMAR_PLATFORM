# 08 DOCUMENT TO CODE TEST RUNBOOK LINKAGE BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline for linking documents to code targets, test targets, and runbook targets
Rule: documentation should become linkable to implementation and validation surfaces so future JARVIS can move from policy to code and verification coherently

---

## 1. Purpose

This document defines the doc-to-code/test/runbook linkage baseline of the platform.

It exists to preserve:
- future codegen readiness
- better traceability from document to implementation
- clearer connection between law, code, tests, and operator action
- a stable base for later registry enrichment

---

## 2. Linkage Principle

Documentation should increasingly support fields such as:
- code_targets
- test_targets
- runbook_targets

This linkage may begin in the registry before it is added everywhere in document headers.

---

## 3. Required Rule

The platform does not need full linkage retroactively today.
But new document governance must make room for it immediately.

---

## 4. What Is Forbidden

The following remain forbidden:
- building a huge docs universe with no path to implementation linkage
- forcing future JARVIS to guess which code or tests a document governs
- treating code, tests, and runbooks as disconnected from documentation
- assuming human memory can remain the only map forever

---

## 5. Final Rule

A mature platform documentation system should eventually point not only to meaning, but to implementation and verification.

---

## 6. Status

This document is the active canonical doc-to-code/test/runbook linkage baseline until replaced by a stricter traceability standard.
