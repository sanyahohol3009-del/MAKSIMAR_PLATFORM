# VISUAL SHELL HANDOFF RULE v1

Status: active shell handoff rule
Scope: first shell-facing visual handoff boundary
Rule: shell handoff does not permit uncontrolled runtime UI shortcuts

---

## 1. Purpose

This document defines the rule for the first shell handoff boundary.

It exists to prevent:
- direct jumps from visual contracts into ad-hoc UI execution
- shell shortcuts that bypass truth-bound visual layers
- uncontrolled presentation hacks

---

## 2. What Is Already True

At this stage, the project has reached:

- display output boundary
- shell handoff boundary

This means a canonical downstream path now exists from visual truth to shell-facing handoff.

---

## 3. What This Boundary Means

This boundary means:

- shell-facing handoff is now contract-backed
- shell-facing handoff is still read-only
- shell-facing handoff is still downstream
- shell-facing handoff does not yet imply uncontrolled UI ownership

---

## 4. What Is Allowed After This Boundary

After this boundary, the project may continue into:

- controlled presentation boundary contracts
- controlled shell-facing presentation assembly
- first honest presented visual result path

---

## 5. What Is Still Forbidden

The following remain forbidden:

- shell-owned truth
- shell-owned execution shortcuts
- ad-hoc runtime rendering hacks
- bypass of visual result path
- UI mutation authority

---

## 6. Final Rule

A shell-facing handoff must remain as honest as the visual contracts that produced it.

If shell integration weakens traceability, truth, or control boundaries, it is rejected.

---

## 7. Status

This document is the active rule for the first shell handoff boundary until replaced by a stricter shell presentation standard.
