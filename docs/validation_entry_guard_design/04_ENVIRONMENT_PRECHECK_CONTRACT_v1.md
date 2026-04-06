# 04 ENVIRONMENT PRECHECK CONTRACT v1

Status: active canonical environment-precheck contract
Scope: design contract for interpreter and toolchain validation before test launch
Rule: environment precheck behavior must remain explicit so full-suite validation is not trusted under ambiguous shell state

---

## 1. Purpose

This document defines the environment-precheck contract of the platform.

It exists to preserve:
- explicit interpreter validation
- explicit pytest-binary validation
- clean rejection of ambiguous toolchain state
- a stable base for later precheck implementation

---

## 2. Contract Principle

Environment precheck design should remain understandable in terms of:
- active environment expectation
- expected Python path behavior
- expected pytest path behavior
- what counts as acceptable resolution
- what counts as rejection-worthy ambiguity

---

## 3. Required Rule

Environment precheck design should remain:
- explicit
- interpreter-aware
- tool-aware
- lightweight
- diagnosable

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting unknown shell state
- silently mixing global and virtualenv tools
- implementation with unreadable environment assumptions
- weak rejection semantics for ambiguous tool resolution

---

## 5. Final Rule

A mature validation guard verifies its toolchain before it trusts its output.

---

## 6. Status

This document is the active canonical environment-precheck contract until replaced by a stricter environment verification reference.
