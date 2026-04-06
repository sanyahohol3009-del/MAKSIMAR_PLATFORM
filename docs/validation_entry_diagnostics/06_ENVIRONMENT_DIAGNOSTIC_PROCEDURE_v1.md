# 06 ENVIRONMENT DIAGNOSTIC PROCEDURE v1

Status: active canonical environment-diagnostic procedure
Scope: diagnosis of environment and toolchain ambiguity before validation launch
Rule: environment diagnostics must remain explicit so validation results are not trusted under the wrong interpreter or wrong pytest binary

---

## 1. Purpose

This document defines the environment-diagnostic procedure of the platform.

It exists to preserve:
- readable diagnosis of environment mismatch
- quick verification of active interpreter and pytest binary
- lower ambiguity in full-suite validation
- a stable base for later environment-guard hardening

---

## 2. Procedure Principle

Environment diagnosis should remain understandable in terms of:
- active virtual environment
- `which python`
- `which pytest`
- consistency between intended and actual tool resolution
- shell state matching canonical validation expectations

---

## 3. Required Rule

Environment diagnostics should remain:
- explicit
- interpreter-aware
- toolchain-aware
- diagnosable
- suitable before large validation runs

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting unknown shell state
- mixing global and virtualenv tools casually
- interpreting validation red output before tool resolution is known
- assuming the active environment without checking it

---

## 5. Final Rule

A mature validation flow verifies its tools before it trusts its verdict.

---

## 6. Status

This document is the active canonical environment-diagnostic procedure until replaced by a stricter environment diagnostics reference.
