# 05 OPEN GAPS RESTART RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for recovering open package gaps efficiently during restart
Rule: open package gaps must remain restart-readable so unfinished work can resume deliberately instead of being rediscovered after every pause

---

## 1. Purpose

This document defines the open-gaps-restart rule of the platform.

It exists to preserve:
- readable unfinished-work recovery
- lower ambiguity around what still remains
- continuity between package closure and resumed next work
- a stable base for later restart hardening

---

## 2. Gaps Principle

Open gaps restart should remain understandable in terms of:
- what remains incomplete
- what kind of future work is still expected
- what is blocked versus merely pending
- how gap recovery preserves continuity

---

## 3. Required Rule

Open gaps restart should remain:
- explicit
- selective
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- unfinished work rediscovered only by rereading
- gap recovery overloaded with weak or irrelevant details
- open-gaps restart meaning preserved only in operator memory
- restart that hides what still remains

---

## 5. Final Rule

A mature documentation system keeps package open gaps restart-readable before pauses turn pending work into drift.

---

## 6. Status

This document is the active canonical open-gaps-restart rule until replaced by a stricter restart reference.
