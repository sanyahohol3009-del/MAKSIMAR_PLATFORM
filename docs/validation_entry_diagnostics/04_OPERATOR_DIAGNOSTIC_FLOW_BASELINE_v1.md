# 04 OPERATOR DIAGNOSTIC FLOW BASELINE v1

Status: active canonical operator-diagnostic-flow baseline
Scope: operator-facing flow for diagnosing validation entry problems in a stable order
Rule: operator diagnostics must remain ordered so investigation starts from the most foundational launch conditions first

---

## 1. Purpose

This document defines the operator-diagnostic-flow baseline of the platform.

It exists to preserve:
- readable operator followup order
- reduced random debugging
- explicit progression from foundational checks to narrower checks
- a stable base for later runbook hardening

---

## 2. Flow Principle

Operator diagnostics should remain understandable in terms of this general order:

1. verify repository root
2. verify active environment
3. verify interpreter and pytest resolution
4. verify trusted entrypoint choice
5. verify execution mode choice
6. only then interpret collection or execution behavior

This sequence preserves diagnostic clarity.

---

## 3. Required Rule

Operator-diagnostic flow should remain:
- explicit
- ordered
- bootstrap-first
- reproducible
- suitable for restart after context loss

---

## 4. What Is Forbidden

The following remain forbidden:
- random debugging order
- jumping to code blame before launch checks
- skipping root or environment verification
- treating operator memory as sufficient diagnostic protocol

---

## 5. Final Rule

A mature platform debugs validation entry from the outside in, not from panic inward.

---

## 6. Status

This document is the active canonical operator-diagnostic-flow baseline until replaced by a stricter validation diagnostics runbook.
