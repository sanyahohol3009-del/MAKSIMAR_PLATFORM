# 06 ENVIRONMENT ACTIVATION DISCIPLINE v1

Status: active canonical environment-activation discipline
Scope: disciplined interpreter and tool selection before validation
Rule: environment activation must remain explicit so operators do not validate with the wrong Python or wrong pytest binary

---

## 1. Purpose

This document defines the environment-activation discipline of the platform.

It exists to preserve:
- correct interpreter selection
- correct pytest binary selection
- repeatable local validation context
- reduced ambiguity during diagnostics

---

## 2. Environment Principle

Environment activation should remain understandable in terms of:
- active virtual environment
- Python executable path
- pytest executable path
- consistency between shell state and validation expectations

---

## 3. Confirmed Expected State

Current validated local pattern included:
- active `.venv`
- `which python` pointing into `.venv`
- `which pytest` pointing into `.venv`

---

## 4. What Is Forbidden

The following remain forbidden:
- mixing global and virtualenv tools casually
- running full-suite validation with unknown interpreter state
- assuming shell state without checking it
- trusting results from ambiguous tool resolution

---

## 5. Final Rule

A mature platform validates with the intended interpreter, not whichever one answered first.

---

## 6. Status

This document is the active canonical environment-activation discipline until replaced by a stricter validation environment reference.
