# 03 PRECHECK FAILURE CLASSIFICATION v1

Status: active canonical precheck-failure classification
Scope: classification of validation failures that occur during prechecks before collection
Rule: precheck failures must remain classified so operators can distinguish root, environment, and entrypoint problems clearly

---

## 1. Purpose

This document defines the precheck-failure classification of the platform.

It exists to preserve:
- structured diagnosis before test collection
- explicit precheck-stage meaning
- bounded interpretation of failed launch conditions
- a stable base for later precheck diagnostics procedures

---

## 2. Classification Principle

Precheck failure should remain understandable in terms of:
- repository-root failure
- environment-resolution failure
- interpreter or pytest-path mismatch
- entrypoint-policy failure
- execution-mode suitability failure

These are pre-execution failures, not executed test failures.

---

## 3. Required Rule

Precheck-failure classification should remain:
- explicit
- category-aware
- pre-execution aware
- diagnosable
- aligned with validation entry discipline

---

## 4. What Is Forbidden

The following remain forbidden:
- one giant undifferentiated precheck failure bucket
- interpreting every early red state the same way
- treating precheck failure as assertion failure
- losing diagnostic order before collection starts

---

## 5. Final Rule

A mature platform classifies precheck failures before it escalates them.

---

## 6. Status

This document is the active canonical precheck-failure classification until replaced by a stricter entry-precheck reference.
