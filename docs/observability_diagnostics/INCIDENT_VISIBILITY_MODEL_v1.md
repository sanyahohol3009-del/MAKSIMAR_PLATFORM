# INCIDENT VISIBILITY MODEL v1

Status: active canonical incident visibility model
Scope: how incident meaning becomes visible to operators
Rule: incidents must remain visible as explicit operational states rather than disappearing into logs, symptoms, or vague failure feelings

---

## 1. Purpose

This document defines the current incident visibility model of the platform.

It exists to preserve clarity about:
- what makes an incident visible
- why incident visibility matters
- how incident meaning differs from ordinary runtime observation
- why visibility must support followup and diagnostics continuity

---

## 2. Incident Visibility Principle

Incident visibility is not only “error exists.”

It should preserve visibility of:
- incident existence
- likely severity or seriousness
- affected runtime context
- relation to degraded or failed state
- connection to followup or recovery thinking

---

## 3. Required Rule

The platform should remain able to make incident meaning visible enough that an operator can distinguish:
- ordinary runtime state
- degraded runtime state
- incident-bearing runtime state
- failure or post-incident state

---

## 4. What Is Forbidden

The following remain forbidden:
- incidents disappearing into raw logs only
- operator awareness depending only on memory or luck
- failure meaning reduced to generic “something broke”
- incident visibility detached from runtime context

---

## 5. Final Rule

A mature platform makes incidents visible in structured form, not only discoverable by accident.

---

## 6. Status

This document is the active canonical incident visibility model until replaced by a stricter incident visibility reference.
