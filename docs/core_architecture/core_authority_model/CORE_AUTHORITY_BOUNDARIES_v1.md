# CORE AUTHORITY BOUNDARIES v1

Status: active canonical authority-boundary rule
Scope: forbidden authority drift across core platform layers
Rule: platform layers must not silently inherit or assume authority that belongs to another layer

---

## 1. Purpose

This document defines the main forbidden authority crossings in the platform.

It exists to prevent:
- presentation layers acting like control planes
- diagnostics layers acting like truth owners
- extensions redefining foundational rules
- convenience-driven authority drift

---

## 2. Core Boundary Families

Important authority boundaries include:

- contracts/rules vs execution
- governance vs presentation
- runtime vs dashboard
- truth sources vs summaries
- optional extensions vs foundational legitimacy

---

## 3. Required Rule

A downstream layer may:
- read
- summarize
- display
- classify

It may not silently:
- redefine
- override
- replace
- own

unless an explicit architecture rule says so.

---

## 4. Forbidden Authority Drift Examples

The following remain forbidden:
- UI as control authority
- dashboard as truth authority
- observability summary as canonical state
- accelerator extension as required legitimacy
- convenience layer becoming hidden system root

---

## 5. Final Rule

Authority boundaries must stay visible if the platform is to remain safe and explainable.

---

## 6. Status

This document is the active canonical authority-boundary rule until replaced by a stricter authority separation standard.
