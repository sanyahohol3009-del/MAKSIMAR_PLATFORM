# DIAGNOSTIC FOLLOWUP ORIENTATION v1

Status: active canonical diagnostic-followup orientation
Scope: what diagnostics should support after health, degraded, or incident visibility appears
Rule: diagnostics must remain useful for followup thinking rather than ending at raw visibility alone

---

## 1. Purpose

This document defines the diagnostic followup orientation of the platform.

It exists to preserve clarity about:
- why visibility alone is not enough
- how diagnostics should support next-step thinking
- why bounded followup matters after degraded or incident signals appear

---

## 2. Followup Principle

Diagnostics should not stop at “something seems wrong.”

They should support understanding of:
- what likely changed
- what context matters
- whether inspection, recovery, or deeper analysis is appropriate
- how downstream operator reasoning remains tied to upstream signals and truth

---

## 3. Required Rule

Diagnostic followup should remain:
- bounded
- explainable
- source-aware
- oriented toward legitimate next steps
- distinct from ungoverned action or panic response

---

## 4. What Is Forbidden

The following remain forbidden:
- diagnostics that only create anxiety without structured meaning
- followup that ignores signal origin and runtime context
- jumping from visibility to action with no bounded interpretation
- losing incident or degraded meaning during downstream explanation

---

## 5. Final Rule

Diagnostics should help operators move from visibility to understanding, not from uncertainty to guesswork.

---

## 6. Status

This document is the active canonical diagnostic-followup orientation until replaced by a stricter diagnostics followup reference.
