# 03 PYTEST ENTRYPOINT POLICY v1

Status: active canonical pytest-entrypoint policy
Scope: canonical pytest launch modes for repository validation
Rule: pytest entrypoints must remain explicitly interpreted so operators do not confuse weaker and stronger launch modes

---

## 1. Purpose

This document defines the pytest-entrypoint policy of the platform.

It exists to preserve:
- clear interpretation of supported launch modes
- continuity between local validation and whole-repo validation
- stable fallback behavior
- a readable base for later automation and CI/CD binding

---

## 2. Entrypoint Principle

Pytest entrypoints should remain understandable in terms of:
- default reliability
- import visibility behavior
- suitability for full-suite execution
- suitability for fallback execution

The current confirmed entrypoints are:

- `python -m pytest -q`
- `PYTHONPATH="$PWD" pytest -q`
- `PYTHONPATH="$PWD" pytest -q -n auto`

---

## 3. Current Canonical Interpretation

Current preferred full-suite fast execution:
- `PYTHONPATH="$PWD" pytest -q -n auto`

Current strong fallback execution:
- `python -m pytest -q`

---

## 4. What Is Forbidden

The following remain forbidden:
- treating every pytest launch form as equivalent
- using ambiguous launch modes without interpretation
- forgetting fallback execution discipline
- trusting broken collection from weaker bootstrap modes

---

## 5. Final Rule

A serious platform names its canonical validation entrypoints explicitly.

---

## 6. Status

This document is the active canonical pytest-entrypoint policy until replaced by a stricter validation launch policy.
