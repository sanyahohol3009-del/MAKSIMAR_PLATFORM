# 02 RESTART BOUNDARY SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how restart boundaries should be bounded and interpreted across documentation packages
Rule: restart-boundary scope must remain explicit so reentry framing stays bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the restart-boundary-scope rule of the platform.

It exists to preserve:
- bounded restart framing
- lower ambiguity around what initial reentry should cover
- continuity between package role and restart discipline
- a stable base for later boundary hardening

---

## 2. Scope Principle

Restart-boundary scope should remain understandable in terms of:
- what initial restart must include
- what remains outside early reentry scope
- what boundary level is primary
- how scope differs across package families

---

## 3. Required Rule

Restart-boundary scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined restart boundaries
- initial restart treated as full package replay
- scope growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature restart layer first defines the scope of safe early reentry before it relies on restart quality.

---

## 6. Status

This document is the active canonical restart-boundary-scope rule until replaced by a stricter scope reference.
