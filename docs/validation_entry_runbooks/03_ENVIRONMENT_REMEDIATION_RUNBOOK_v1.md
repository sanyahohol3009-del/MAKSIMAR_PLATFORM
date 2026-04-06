# 03 ENVIRONMENT REMEDIATION RUNBOOK v1

Status: active canonical environment-remediation runbook
Scope: operator recovery when validation is launched with ambiguous or incorrect interpreter/tool state
Rule: environment problems must be corrected before validation meaning is trusted again

---

## 1. Purpose

This document defines the environment-remediation runbook of the platform.

It exists to preserve:
- explicit interpreter correction
- explicit pytest-binary correction
- lower ambiguity during validation recovery
- a stable base for later environment-check automation

---

## 2. Remediation Principle

Environment remediation should remain understandable in terms of:
- identifying the wrong or ambiguous interpreter state
- restoring the intended virtual environment
- rechecking Python and pytest paths
- relaunching validation only after toolchain clarity is restored

---

## 3. Required Rule

Environment remediation should remain:
- explicit
- interpreter-aware
- tool-aware
- repeatable
- diagnostics-consistent

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting validation from ambiguous environment state
- mixing global and virtualenv tools casually
- skipping rechecks after environment correction
- interpreting tool-resolution errors as code failure

---

## 5. Final Rule

A mature validation workflow fixes the toolchain before it judges the code.

---

## 6. Status

This document is the active canonical environment-remediation runbook until replaced by a stricter environment recovery reference.
