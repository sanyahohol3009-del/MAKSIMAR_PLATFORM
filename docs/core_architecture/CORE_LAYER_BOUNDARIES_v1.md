# CORE LAYER BOUNDARIES v1

Status: active canonical layer boundary rule
Scope: separation of major platform layers
Rule: core platform layers must remain explicitly separated so truth, control, execution, observability, and presentation do not collapse into one another

---

## 1. Purpose

This document defines the main layer boundaries of the core platform.

It exists to prevent:
- control/execution confusion
- dashboard/runtime confusion
- policy/compute confusion
- truth/presentation confusion

---

## 2. Canonical Boundary Families

The platform must preserve boundaries such as:

- core contracts / canonical models
- runtime application behavior
- execution control
- observability and diagnostics
- dashboard / presentation
- mobile / external bridges
- future engine adapters and heavy compute paths

---

## 3. Key Boundary Principle

Important separations include:
- control ≠ execution
- execution ≠ observability
- observability ≠ dashboard
- dashboard ≠ source of truth
- policy ≠ compute
- bridge ≠ backend implementation

---

## 4. Required Rule

A downstream layer may read, summarize, or present upstream truth,
but it must not silently redefine that truth.

---

## 5. What Is Forbidden

The following remain forbidden:
- dashboards acting as truth owners
- control logic hidden inside presentation layers
- compute logic hidden inside policy layers
- undocumented layer collapse

---

## 6. Final Rule

Layer clarity is part of platform safety and continuity.

---

## 7. Status

This document is the active canonical layer boundary rule until replaced by a stricter boundary specification.
