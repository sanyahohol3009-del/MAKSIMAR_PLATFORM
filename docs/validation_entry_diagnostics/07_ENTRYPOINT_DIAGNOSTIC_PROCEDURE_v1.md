# 07 ENTRYPOINT DIAGNOSTIC PROCEDURE v1

Status: active canonical entrypoint-diagnostic procedure
Scope: diagnosis of whether validation was launched through a trusted or ambiguous command path
Rule: entrypoint diagnostics must remain explicit so operators can distinguish command ambiguity from repository failure

---

## 1. Purpose

This document defines the entrypoint-diagnostic procedure of the platform.

It exists to preserve:
- readable diagnosis of launch-command quality
- continuity between canonical entrypoint policy and operator behavior
- lower confusion when one launch form fails and another succeeds
- a stable base for later command enforcement diagnostics

---

## 2. Procedure Principle

Entrypoint diagnosis should remain understandable in terms of:
- which command was used
- whether that command is canonical
- whether it is fast-path or fallback-path
- whether import visibility depends on that choice
- whether failure meaning changes with the command form

---

## 3. Required Rule

Entrypoint diagnostics should remain:
- explicit
- command-aware
- bootstrap-aware
- fallback-aware
- suitable for operator interpretation

---

## 4. What Is Forbidden

The following remain forbidden:
- treating all command forms as equal without checking them
- forgetting which entrypoint produced which result
- blaming code when launch semantics differ
- relying on command memory instead of written interpretation

---

## 5. Final Rule

A mature platform checks how validation was launched before it decides how serious the failure is.

---

## 6. Status

This document is the active canonical entrypoint-diagnostic procedure until replaced by a stricter validation launch diagnostics reference.
