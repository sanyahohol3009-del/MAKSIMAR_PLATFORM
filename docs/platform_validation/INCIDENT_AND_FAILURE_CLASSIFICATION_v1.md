# INCIDENT AND FAILURE CLASSIFICATION v1

Status: active canonical validation incident rule
Scope: failed checks, flaky checks, degraded checks, runtime anomalies
Rule: validation failures must be classified before remediation is chosen

---

## 1. Purpose

This document defines canonical classification of validation incidents.

It exists to prevent:
- panic-driven debugging
- wrong remediation
- confusion between code defects and environment defects
- confusion between runtime failures and validation failures

---

## 2. Canonical Failure Classes

Failures may belong to categories such as:
- code defect
- test defect
- isolation defect
- environment defect
- worker/process defect
- flaky timing defect
- runtime consistency defect
- documentation or contract drift

---

## 3. Required Rule

A failed validation event should be classified before major architectural conclusions are made.

---

## 4. Required Outputs

Classification should support:
- short failure summary
- failure class
- reproducibility note
- suggested next diagnostic tier

---

## 5. Final Rule

Not every red result means the same thing.
Classification is required before confidence.

---

## 6. Status

This document is the active canonical validation incident rule until replaced by a stricter diagnostic governance standard.
