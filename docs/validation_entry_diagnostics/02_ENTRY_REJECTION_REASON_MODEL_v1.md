# 02 ENTRY REJECTION REASON MODEL v1

Status: active canonical entry-rejection-reason model
Scope: structured interpretation of why a validation launch may be rejected before execution
Rule: entry rejection reasons must remain nameable so enforced launch rejection is interpretable instead of looking arbitrary

---

## 1. Purpose

This document defines the entry-rejection-reason model of the platform.

It exists to preserve:
- readable rejection semantics
- explicit distinction among rejection causes
- continuity between enforcement and diagnostics
- a stable base for later coded rejection reporting

---

## 2. Rejection Principle

Entry rejection should remain understandable in terms of:
- wrong repository root
- invalid environment state
- untrusted entrypoint
- invalid execution-mode choice
- other bootstrap condition failure

A rejected launch should say what boundary was not met.

---

## 3. Required Rule

Entry rejection reasons should remain:
- explicit
- bounded
- stage-aware
- enforcement-aware
- suitable for operator followup

---

## 4. What Is Forbidden

The following remain forbidden:
- generic rejection with no readable reason
- collapsing different rejection causes into one vague failure
- treating rejected launch as a code defect by default
- letting rejection semantics live only in future code

---

## 5. Final Rule

A mature validation system names why entry was rejected.

---

## 6. Status

This document is the active canonical entry-rejection-reason model until replaced by a stricter rejection diagnostics reference.
