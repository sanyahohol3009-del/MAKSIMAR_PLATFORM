# SHARED NOTHING DEFAULT RULE v1

Status: active canonical shared-nothing rule
Scope: concurrent execution, workers, nodes, future swarm logic
Rule: shared mutable state is forbidden by default; coordination must be explicit

---

## 1. Purpose

This document defines the canonical shared-nothing-by-default rule.

It exists to prevent:
- hidden shared-state corruption
- nondeterministic worker interference
- concurrency bugs hidden behind convenience

---

## 2. Default Principle

By default:
- no shared mutable state
- no implicit global coordination
- no silent ownership ambiguity

Preferred design:
- immutable contracts
- artifact references
- explicit handoff
- explicit coordination
- namespaced resources

---

## 3. Allowed Exceptions

Exceptions must be:
- explicit
- justified
- bounded
- observable
- recoverable

---

## 4. What Is Forbidden

The following remain forbidden:
- shared mutable truth
- implicit cross-worker memory ownership
- convenience globals controlling concurrent flows
- hidden caches that alter correctness

---

## 5. Final Rule

Shared mutable state is the exception.
Isolation is the default.

---

## 6. Status

This document is the active canonical shared-nothing rule until replaced by a stricter distributed state standard.
