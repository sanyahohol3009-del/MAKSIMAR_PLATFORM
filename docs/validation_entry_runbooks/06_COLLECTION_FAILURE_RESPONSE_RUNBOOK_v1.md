# 06 COLLECTION FAILURE RESPONSE RUNBOOK v1

Status: active canonical collection-failure-response runbook
Scope: operator response when pytest fails during collection rather than executed assertions
Rule: collection-stage failure must be handled as an entry and bootstrap interpretation problem first

---

## 1. Purpose

This document defines the collection-failure-response runbook of the platform.

It exists to preserve:
- stage-correct response to collection failure
- lower panic during large red output
- distinction between bootstrap failure and code logic failure
- a stable base for later validation incident procedures

---

## 2. Response Principle

Collection-failure response should remain understandable in terms of:
- confirming that execution did not reach real assertion evaluation
- checking import visibility and entry conditions
- correcting bootstrap issues first
- rerunning trusted commands only after entry meaning is restored

---

## 3. Required Rule

Collection-failure response should remain:
- explicit
- stage-aware
- bootstrap-aware
- recovery-oriented
- diagnostics-consistent

---

## 4. What Is Forbidden

The following remain forbidden:
- treating collection-stage error counts as equal numbers of independent code defects
- beginning deep debugging before bootstrap checks
- panic-driven interpretation of red output
- skipping rerun under trusted conditions

---

## 5. Final Rule

A mature validation workflow first asks whether tests actually started before it judges why they failed.

---

## 6. Status

This document is the active canonical collection-failure-response runbook until replaced by a stricter collection recovery reference.
