# PARALLEL TEST RUNTIME PROFILE RULE v1

Status: active canonical parallel test runtime profile rule
Scope: pytest runtime modes for local and future CI execution
Rule: parallel test execution must use explicit runtime profiles with a stable serial fallback

---

## 1. Purpose

This document defines the canonical runtime profiles for test execution.

It exists to prevent:
- random test launch modes
- unsafe automatic scaling assumptions
- confusion between safe bounded mode and hardware-scaled mode
- loss of serial fallback discipline

---

## 2. Canonical Test Runtime Profiles

### 2.1 Serial mode
Command form:
`python -m pytest tests -q`

Meaning:
- canonical fallback mode
- debugging mode
- correctness fallback
- used when isolation is uncertain

### 2.2 Bounded parallel mode
Command form:
`python -m pytest tests -n 2 -q`

Meaning:
- conservative parallel verification
- first escalation from serial mode
- recommended first check after enabling xdist
- safe-mode parallel profile

### 2.3 Hardware-scaled parallel mode
Command form:
`python -m pytest tests -n auto -q`

Meaning:
- hardware-aware parallel execution
- performance-oriented full-suite run
- preferred mode when bounded mode is already stable

---

## 3. Required Usage Order

The preferred order is:

1. serial mode
2. bounded parallel mode
3. hardware-scaled parallel mode

Do not promote a suite directly to hardware-scaled mode unless bounded mode is already stable.

---

## 4. Required Fallback Rule

Serial mode must always remain available.

If bounded or hardware-scaled mode fails in a way that suggests contention, isolation drift, or worker instability:
- fall back to serial mode
- diagnose
- correct
- retry parallel mode later

---

## 5. Hardware Neutrality

This rule must remain valid on:
- weak developer machines
- general desktops
- strong workstations
- high-core servers
- future cluster-like environments

The runtime profile names stay valid even when the hardware changes.

---

## 6. What Is Forbidden

The following remain forbidden:
- assuming one runtime profile for all hardware
- deleting serial mode from project discipline
- jumping straight to large-scale parallelism without bounded verification
- treating auto-parallel as correctness proof by itself

---

## 7. Final Rule

Parallel execution is encouraged.
Parallel execution must remain controlled.
Serial execution remains the correctness fallback.

---

## 8. Status

This document is the active canonical parallel test runtime profile rule until replaced by a stricter test execution standard.
