# 06 REJECTION MESSAGE SCHEMA BASELINE v1

Status: active canonical rejection-message-schema baseline
Scope: readable structure for future validation-entry rejection output
Rule: rejection output must remain structured so operators can understand what failed and what to do next

---

## 1. Purpose

This document defines the rejection-message-schema baseline of the platform.

It exists to preserve:
- readable rejection output structure
- stage-aware failure communication
- reduced panic during rejected validation entry
- a stable base for later structured output implementation

---

## 2. Schema Principle

Rejection-message design should remain understandable in terms of:
- what stage failed
- what condition was expected
- what condition was observed
- what next corrective step is recommended
- whether fallback remains available

---

## 3. Required Rule

Rejection-message design should remain:
- explicit
- short enough to read
- structured enough to diagnose
- operator-oriented
- consistent with diagnostics and runbook families

---

## 4. What Is Forbidden

The following remain forbidden:
- vague rejection output
- red output with no stage meaning
- implementation messages that require source reading to understand
- rejection semantics preserved only in code comments

---

## 5. Final Rule

A mature validation guard rejects clearly, not cryptically.

---

## 6. Status

This document is the active canonical rejection-message-schema baseline until replaced by a stricter structured output reference.
