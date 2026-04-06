# 05 ENTRYPOINT SELECTION CONTRACT v1

Status: active canonical entrypoint-selection contract
Scope: design contract for accepted, preferred, and fallback validation launch modes
Rule: entrypoint selection must remain explicit so future guard code preserves canonical validation meaning

---

## 1. Purpose

This document defines the entrypoint-selection contract of the platform.

It exists to preserve:
- explicit acceptance of trusted commands
- explicit distinction between preferred and fallback modes
- reduced command ambiguity
- a stable base for later entrypoint-selection implementation

---

## 2. Contract Principle

Entrypoint-selection design should remain understandable in terms of:
- what commands are accepted
- what command is preferred for fast full-suite execution
- what command remains correctness-first fallback
- what commands are too ambiguous to trust

---

## 3. Required Rule

Entrypoint-selection design should remain:
- explicit
- command-aware
- fallback-aware
- bootstrap-aware
- aligned with canonical validation documentation

---

## 4. What Is Forbidden

The following remain forbidden:
- treating all launch forms as equivalent
- silent acceptance of ambiguous commands
- forgetting the distinction between fast and fallback paths
- command drift between docs and future code

---

## 5. Final Rule

A mature validation guard knows which launch modes are legitimate.

---

## 6. Status

This document is the active canonical entrypoint-selection contract until replaced by a stricter entrypoint-control reference.
