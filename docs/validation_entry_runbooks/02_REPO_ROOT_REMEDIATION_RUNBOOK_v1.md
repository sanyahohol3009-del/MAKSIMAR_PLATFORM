# 02 REPO ROOT REMEDIATION RUNBOOK v1

Status: active canonical repo-root-remediation runbook
Scope: operator recovery when validation is launched from the wrong repository location
Rule: wrong-root validation must be corrected explicitly so bootstrap meaning is restored before test interpretation continues

---

## 1. Purpose

This document defines the repo-root-remediation runbook of the platform.

It exists to preserve:
- explicit correction of wrong-root launches
- restoration of repo-aware validation meaning
- lower confusion during entry-stage failures
- a stable base for later root-guard automation

---

## 2. Remediation Principle

Repo-root remediation should remain understandable in terms of:
- detecting that execution started from the wrong location
- restoring the correct project root
- rechecking command context
- retrying validation only after root meaning is restored

---

## 3. Required Rule

Repo-root remediation should remain:
- explicit
- lightweight
- repeatable
- diagnostics-aligned
- easy for an operator to execute

---

## 4. What Is Forbidden

The following remain forbidden:
- continuing validation from the wrong folder
- interpreting wrong-root failures as domain failures
- retrying blindly without root correction
- trusting partial output from invalid launch context

---

## 5. Final Rule

A mature validation workflow restores the right root before it trusts the next result.

---

## 6. Status

This document is the active canonical repo-root-remediation runbook until replaced by a stricter repo-root recovery reference.
