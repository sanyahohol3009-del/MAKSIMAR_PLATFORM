# 04 REPO ROOT PRECHECK BASELINE v1

Status: active canonical repo-root-precheck baseline
Scope: pre-execution checking of repository-root correctness before validation launch
Rule: repo-root correctness should be checked before validation begins so wrong-directory execution is rejected early

---

## 1. Purpose

This document defines the repo-root-precheck baseline of the platform.

It exists to preserve:
- early repo-root verification
- reduced wrong-directory execution risk
- cleaner launch interpretation
- a stable base for later root-guard implementation

---

## 2. Precheck Principle

Repo-root precheck should remain understandable in terms of:
- expected root location
- expected project identity markers
- early detection of wrong shell context
- prevention of misleading validation behavior

---

## 3. Required Rule

Repo-root precheck should remain:
- explicit
- fast
- readable
- validation-oriented
- suitable for wrapper and CI use

---

## 4. What Is Forbidden

The following remain forbidden:
- trusting current shell location without verification
- allowing full validation to begin from an invalid root
- hiding repo-root assumptions
- accepting wrong-directory execution as harmless

---

## 5. Final Rule

A mature validation entry checks where it stands before it decides what to run.

---

## 6. Status

This document is the active canonical repo-root-precheck baseline until replaced by a stricter root-verification reference.
