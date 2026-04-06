# 06 ENTRYPOINT SELECTION ENFORCEMENT v1

Status: active canonical entrypoint-selection-enforcement baseline
Scope: enforcement-oriented selection of accepted validation launch modes
Rule: accepted validation entrypoints must remain explicitly constrained so launch ambiguity does not weaken validation meaning

---

## 1. Purpose

This document defines the entrypoint-selection-enforcement baseline of the platform.

It exists to preserve:
- explicit acceptance of trusted launch modes
- rejection of ambiguous validation entry behavior
- continuity between canonical command policy and enforceable practice
- a stable base for later wrapper and CI binding

---

## 2. Selection Principle

Entrypoint-selection enforcement should remain understandable in terms of:
- what entrypoints are accepted
- what entrypoints are preferred
- what entrypoints remain fallback-only
- what launch modes are too ambiguous to trust
- how selection preserves validation legitimacy

---

## 3. Required Rule

Entrypoint-selection enforcement should remain:
- explicit
- command-aware
- bootstrap-aware
- fallback-aware
- aligned with canonical validation documentation

---

## 4. What Is Forbidden

The following remain forbidden:
- treating all launch forms as equivalent
- silent acceptance of ambiguous validation commands
- forgetting the distinction between fast path and correctness-first fallback
- convenience-based drift away from trusted entrypoints

---

## 5. Final Rule

A mature validation system does not merely allow commands.
It names which ones are legitimate.

---

## 6. Status

This document is the active canonical entrypoint-selection-enforcement baseline until replaced by a stricter validation command enforcement reference.
