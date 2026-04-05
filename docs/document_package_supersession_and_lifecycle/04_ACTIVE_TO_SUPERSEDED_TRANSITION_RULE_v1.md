# 04 ACTIVE TO SUPERSEDED TRANSITION RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: transition rule for moving packages from active to superseded state
Rule: active-to-superseded transitions must remain readable so documentation change does not create silent status decay

---

## 1. Purpose

This document defines the active-to-superseded transition rule of the platform.

It exists to preserve:
- ordered package transition
- lower risk of silent lifecycle drift
- continuity between active meaning and replaced meaning
- a stable base for later lifecycle hardening

---

## 2. Transition Principle

Active-to-superseded transitions should remain understandable in terms of:
- what changed
- why the package is no longer active
- what package now carries the active meaning
- how the transition preserves interpretive trust

---

## 3. Required Rule

Active-to-superseded transitions should remain:
- explicit
- ordered
- readable
- lifecycle-aware
- non-chaotic

---

## 4. What Is Forbidden

The following remain forbidden:
- silent active-state loss
- superseded packages left looking active
- transition logic preserved only in memory
- replacement with no readable trace

---

## 5. Final Rule

A mature documentation system transitions packages deliberately rather than letting status decay by neglect.

---

## 6. Status

This document is the active canonical active-to-superseded transition rule until replaced by a stricter transition reference.
