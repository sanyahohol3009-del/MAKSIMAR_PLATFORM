# CORE AUTHORITY AND TRUTH RELATION v1

Status: active canonical authority/truth relation rule
Scope: how authority relates to source-of-truth across the core platform
Rule: authority over interpretation must not be confused with authority over truth itself

---

## 1. Purpose

This document defines the relationship between authority and truth in the platform.

It exists to prevent:
- summaries becoming truth
- diagnostics becoming truth
- control signals becoming truth
- human/operator convenience redefining authoritative state

---

## 2. Truth vs Authority Principle

Truth and authority are related, but not identical.

Examples:
- a layer may have authority to interpret truth
- a layer may have authority to execute under rules
- a layer may have authority to present truth
- but none of these automatically means authority to redefine truth

---

## 3. Required Rule

Whenever a layer consumes upstream truth, it must remain explainable in terms of:
- what source it read
- what interpretation it applied
- what it is allowed to conclude
- what it is not allowed to replace

---

## 4. Final Rule

Truth stays source-backed.
Authority must remain bounded relative to that truth.

---

## 5. Status

This document is the active canonical authority/truth relation rule until replaced by a stricter truth-authority specification.
