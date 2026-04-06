# 05 ENVIRONMENT PRECHECK BASELINE v1

Status: active canonical environment-precheck baseline
Scope: pre-execution checking of interpreter and toolchain state before validation launch
Rule: environment state should be checked before validation begins so results are not trusted under ambiguous interpreter conditions

---

## 1. Purpose

This document defines the environment-precheck baseline of the platform.

It exists to preserve:
- early interpreter verification
- early pytest-binary verification
- cleaner diagnosis of invalid shell state
- a stable base for later environment guard implementation

---

## 2. Precheck Principle

Environment precheck should remain understandable in terms of:
- active virtual environment
- Python path
- pytest path
- consistency between expected and actual tool resolution
- rejection of ambiguous toolchain state

---

## 3. Required Rule

Environment precheck should remain:
- explicit
- lightweight
- diagnosable
- interpreter-aware
- compatible with canonical validation commands

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting unknown interpreter state
- beginning full-suite validation with ambiguous tool resolution
- mixing global and virtualenv assumptions silently
- accepting environment ambiguity as normal

---

## 5. Final Rule

A mature validation entry checks its toolchain before it trusts its outcome.

---

## 6. Status

This document is the active canonical environment-precheck baseline until replaced by a stricter environment verification reference.
