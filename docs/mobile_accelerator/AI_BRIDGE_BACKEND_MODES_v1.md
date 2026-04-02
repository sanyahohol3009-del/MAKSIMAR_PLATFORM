# AI BRIDGE BACKEND MODES v1

Status: active canonical AI bridge backend modes rule
Scope: local backend, external accelerator backend, degraded fallback
Rule: the mobile app must interact with AI only through a unified bridge contract, regardless of backend mode

---

## 1. Purpose

This document defines canonical backend modes for the mobile AI bridge.

It exists to prevent:
- backend-specific UI logic
- fragile mode switching
- no-fallback accelerator dependence
- hidden compute routing

---

## 2. Canonical Backend Modes

### 2.1 Local Mode
Meaning:
- compute runs on the phone itself
- local Python / local inference backend is active
- used by default when no external accelerator is available

### 2.2 External Accelerator Mode
Meaning:
- compute is routed to MAKSIMAR external accelerator hardware
- the app sees the same bridge interface
- transport and discovery live below the bridge boundary

### 2.3 Safe Degraded Mode
Meaning:
- system reduces capability to preserve usability and safety
- fallback may be triggered by:
  - disconnect
  - thermal pressure
  - battery policy
  - health failure
  - transport instability

---

## 3. Selection Principle

Backend choice must be determined by:

- availability
- health
- policy
- thermal state
- power state
- capability profile
- explicit user policy where applicable

---

## 4. Required Rule

The UI layer must not know whether inference is happening:
- locally
- on an external accelerator
- on a home node

UI consumes bridge outputs only.

---

## 5. What Is Forbidden

The following remain forbidden:

- UI branching on backend internals
- accelerator-only mode without fallback
- hidden backend switching without state visibility
- treating degraded mode as failure instead of controlled fallback

---

## 6. Final Rule

The bridge owns backend selection.
The app consumes one stable AI capability surface.

---

## 7. Status

This document is the active canonical AI bridge backend modes rule until replaced by a stricter mobile/backend routing standard.
