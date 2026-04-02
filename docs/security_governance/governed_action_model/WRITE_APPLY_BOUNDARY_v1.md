# WRITE APPLY BOUNDARY v1

Status: active canonical write/apply boundary rule
Scope: distinction between non-mutating reasoning and mutating/apply behavior
Rule: write/apply behavior must remain visibly distinct from reasoning and proposal behavior

---

## 1. Purpose

This document defines the write/apply boundary in the platform.

It exists to prevent:
- silent writes
- accidental mutation
- operator confusion about what changed and why
- illegitimate escalation from analysis to real effect

---

## 2. Boundary Principle

The platform must distinguish clearly between:
- read
- inspect
- reason
- propose
- simulate
- write/apply

Write/apply behavior is materially more sensitive than inspection or proposal.

---

## 3. Required Rule

Write/apply behavior must not be triggered merely because:
- reasoning completed
- a suggestion seems good
- the UI makes action easy
- a downstream layer assumes approval

---

## 4. What Is Forbidden

The following remain forbidden:
- hidden writes in reasoning-only flows
- proposal screens that silently apply
- mutating behavior framed as passive observation
- ambiguous transitions from preview to apply

---

## 5. Final Rule

A platform stays governable when write/apply behavior remains unmistakably separate.

---

## 6. Status

This document is the active canonical write/apply boundary rule until replaced by a stricter mutating-action boundary specification.
