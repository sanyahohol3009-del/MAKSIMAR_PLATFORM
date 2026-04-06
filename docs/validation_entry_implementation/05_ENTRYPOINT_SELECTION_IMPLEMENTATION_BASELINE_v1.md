# 05 ENTRYPOINT SELECTION IMPLEMENTATION BASELINE v1

Status: active canonical entrypoint-selection implementation baseline
Scope: implementation-facing control of accepted validation launch modes
Rule: accepted validation entrypoints should be implementation-backed so trusted launch modes remain explicit and enforceable

---

## 1. Purpose

This document defines the entrypoint-selection implementation baseline of the platform.

It exists to preserve:
- explicit accepted launch modes
- readable distinction between preferred and fallback paths
- rejection of ambiguous launch modes
- a stable base for later wrapper and guard code

---

## 2. Selection Principle

Entrypoint-selection implementation should remain understandable in terms of:
- accepted commands
- preferred commands
- fallback commands
- rejected commands
- readable explanation for the decision

---

## 3. Required Rule

Entrypoint-selection implementation should remain:
- explicit
- command-aware
- fallback-aware
- diagnostics-aware
- aligned with canonical validation policy

---

## 4. What Is Forbidden

The following remain forbidden:
- treating all launch forms as equivalent
- silent acceptance of weak or ambiguous entrypoints
- forgetting correctness-first fallback interpretation
- hidden selection logic with no readable policy continuity

---

## 5. Final Rule

A mature validation system implements command legitimacy explicitly.

---

## 6. Status

This document is the active canonical entrypoint-selection implementation baseline until replaced by a stricter implementation reference.
