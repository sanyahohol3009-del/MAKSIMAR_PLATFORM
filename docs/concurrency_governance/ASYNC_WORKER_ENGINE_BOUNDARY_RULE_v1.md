# ASYNC WORKER ENGINE BOUNDARY RULE v1

Status: active canonical async/worker/engine boundary rule
Scope: orchestration, worker execution, backend engines
Rule: orchestration, worker control, and heavy compute must remain separated

---

## 1. Purpose

This document defines the canonical boundary between async orchestration, worker shells, and compute engines.

It exists to prevent:
- compute leaking into control-plane logic
- worker shells becoming heavy engines
- policy and compute mixing
- async orchestration becoming blocking compute code

---

## 2. Canonical Split

The preferred split is:

- async orchestration
- worker shell
- engine adapter
- backend engine

---

## 3. Required Behavior

Async layers should:
- orchestrate
- schedule
- coordinate
- observe
- hand off

Engine layers should:
- compute
- transform
- infer
- simulate
- render

---

## 4. What Is Forbidden

The following remain forbidden:
- heavy compute directly in orchestration shell
- policy decisions inside compute backend
- backend-specific leakage into core contracts
- mixing async control and blocking heavy work without boundary

---

## 5. Final Rule

Orchestration coordinates.
Workers host bounded execution.
Engines compute.

---

## 6. Status

This document is the active canonical async/worker/engine boundary rule until replaced by a stricter execution architecture standard.
