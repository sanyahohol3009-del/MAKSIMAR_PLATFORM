# VISUAL CHANGE ACCEPTANCE CHECKLIST v1

Status: active  
Scope: acceptance checklist for each visual polish change  
Rule: every visual change must pass the same truth-preserving acceptance filter

---

## 1. Purpose

This document defines the per-change checklist for visual polish work.

It exists to catch subtle visual drift early.

---

## 2. Required Acceptance Checks

Every visual change must satisfy all of the following:

- readability improved
- operator hierarchy improved or preserved
- truth preserved
- semantics unchanged
- tests green
- no new runtime coupling introduced

---

## 3. Additional Required Questions

For each visual change, ask:

1. Did this change improve clarity?
2. Did this change preserve truth binding?
3. Did this change avoid semantic reinterpretation?
4. Did this change avoid new runtime/control coupling?
5. Did tests remain green?

If any answer is “no”, the change is rejected.

---

## 4. Final Rule

A visual change is accepted only if it improves presentation without weakening truth, readability, or architectural discipline.
