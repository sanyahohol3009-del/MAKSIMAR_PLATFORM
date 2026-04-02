# RESOURCE CONTENTION RULE v1

Status: active canonical resource contention rule
Scope: files, ports, locks, temp data, shared execution resources
Rule: contention must be prevented by design and surfaced when prevention is not possible

---

## 1. Purpose

This document defines the canonical contention rule.

It exists to prevent:
- file collisions
- port collisions
- lock starvation
- worker interference
- hidden race conditions

---

## 2. Shared Resource Principle

Shared resources must be treated as dangerous by default.

Examples:
- files
- sockets
- ports
- caches
- temp directories
- database handles
- external processes

---

## 3. Required Strategy

The preferred order is:

1. isolate
2. partition
3. namespace
4. lock only if unavoidable
5. observe contention explicitly

---

## 4. Required Properties

Where contention is possible, the system must define:
- ownership
- lifetime
- collision policy
- retry policy if any
- timeout policy
- observability hooks

---

## 5. What Is Forbidden

The following remain forbidden:
- silent file collisions
- shared temp directories without namespacing
- hidden lock dependence
- assuming “it is probably fine”
- resource sharing without explicit coordination

---

## 6. Final Rule

Isolation is preferred.
Locking is the fallback.
Silence is forbidden.

---

## 7. Status

This document is the active canonical resource contention rule until replaced by a stricter isolation standard.
