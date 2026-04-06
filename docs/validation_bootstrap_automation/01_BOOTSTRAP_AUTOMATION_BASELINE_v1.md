# 01 BOOTSTRAP AUTOMATION BASELINE v1

Status: active canonical bootstrap-automation baseline
Scope: automation-oriented hardening of validation bootstrap across the repository
Rule: bootstrap automation must remain explicit so trustworthy validation does not depend only on manual shell discipline

---

## 1. Purpose

This document defines the bootstrap-automation baseline of the platform.

It exists to preserve:
- automation-aware validation startup discipline
- reduced dependence on manual operator memory
- stronger repeatability across environments
- a stable base for later wrapper and CI enforcement families

---

## 2. Automation Principle

Bootstrap automation should remain understandable in terms of:
- consistent repo-root execution
- consistent interpreter and pytest selection
- reduced launch ambiguity
- machine-repeatable entry behavior
- preservation of validation trust

Automation should strengthen bootstrap discipline, not hide it.

---

## 3. Required Rule

Bootstrap automation should remain:
- explicit
- repeatable
- repo-root aware
- environment aware
- compatible with canonical validation interpretation

---

## 4. What Is Forbidden

The following remain forbidden:
- relying forever on manual launch memory alone
- automation that hides validation assumptions
- convenience wrappers with ambiguous behavior
- automation that weakens fallback discipline

---

## 5. Final Rule

A mature platform should automate trusted bootstrap, not merely remember it.

---

## 6. Status

This document is the active canonical bootstrap-automation baseline until replaced by a stricter automation reference.
