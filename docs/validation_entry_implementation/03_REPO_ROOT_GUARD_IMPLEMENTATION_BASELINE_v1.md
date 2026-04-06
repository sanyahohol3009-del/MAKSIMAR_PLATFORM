# 03 REPO ROOT GUARD IMPLEMENTATION BASELINE v1

Status: active canonical repo-root-guard implementation baseline
Scope: implementation-facing guarding of repository-root validation startup
Rule: repo-root validation assumptions should be implementation-backed so wrong-root launches are rejected early and readably

---

## 1. Purpose

This document defines the repo-root-guard implementation baseline of the platform.

It exists to preserve:
- early repo-root validation
- rejection of wrong-root execution
- readable pre-launch diagnosis
- a stable base for later concrete root-guard code

---

## 2. Guard Principle

Repo-root guard implementation should remain understandable in terms of:
- expected root condition
- observed launch location
- accept or reject outcome
- readable operator message
- continuity with runbook recovery

---

## 3. Required Rule

Repo-root guard implementation should remain:
- explicit
- lightweight
- early-stage
- readable
- aligned with canonical validation entry rules

---

## 4. What Is Forbidden

The following remain forbidden:
- running full validation from arbitrary directories without interpretation
- hidden root assumptions
- silent wrong-root acceptance
- unreadable rejection behavior

---

## 5. Final Rule

A mature validation system checks where it is before it trusts what it runs.

---

## 6. Status

This document is the active canonical repo-root-guard implementation baseline until replaced by a stricter implementation reference.
