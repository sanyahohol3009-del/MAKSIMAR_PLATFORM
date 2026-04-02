# CORE DOMAIN RESPONSIBILITY MATRIX v1

Status: active canonical domain responsibility matrix
Scope: role boundaries across major platform domains
Rule: each major domain should have a recognizable responsibility focus so architectural drift can be noticed earlier

---

## 1. Purpose

This document provides a first responsibility matrix for core domains.

It exists to prevent:
- domain ambiguity
- overlapping ownership by accident
- unclear architectural expectations

---

## 2. Responsibility Matrix

| Domain | Primary Responsibility |
|---|---|
| Core Contracts / Canonical Models | stable shapes, rules, contracts, invariants |
| Security / Governance | trust boundaries, approval logic, immutable/safe constraints |
| Runtime / Execution Control | live behavior, orchestration, execution flow |
| Observability / Diagnostics | interpret and surface runtime/system condition |
| Validation / Testing / CI-CD | verify integrity, detect regressions, classify failures |
| Visual / Dashboard / Operator Layer | present downstream operator-facing status and system views |
| Mobile / Bridge / Accelerator | extend access, backend routing, external/mobile compute surfaces |
| AI / Memory / Self-Awareness | memory logic, provenance, reflective system understanding |
| Agent / Swarm | multi-agent coordination, capability boundaries, structured parallel behavior |
| Physical AI / Simulation | future physical/simulation-oriented execution and explainable evaluation |

---

## 3. Required Rule

This matrix is a baseline, not the final maximum detail.

Its purpose is to preserve architectural orientation and reduce responsibility confusion.

---

## 4. Final Rule

A domain should be identifiable by its responsibility, not only by its folder name.

---

## 5. Status

This document is the active canonical domain responsibility matrix until replaced by a stricter domain ownership reference.
