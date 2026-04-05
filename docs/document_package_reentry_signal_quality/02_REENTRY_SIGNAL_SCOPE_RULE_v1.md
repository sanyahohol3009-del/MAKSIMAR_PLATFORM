# 02 REENTRY SIGNAL SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how reentry signals should be bounded and interpreted across documentation packages
Rule: reentry-signal scope must remain explicit so restart cues stay bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the reentry-signal-scope rule of the platform.

It exists to preserve:
- bounded restart cues
- lower ambiguity around what signals belong in the initial reentry layer
- continuity between package role and reentry guidance
- a stable base for later signal hardening

---

## 2. Scope Principle

Reentry-signal scope should remain understandable in terms of:
- what signals belong in early reentry
- what signals may remain outside it
- what signal level is primary
- how scope differs across package families

---

## 3. Required Rule

Reentry-signal scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined signal boundaries
- reentry signals treated as full package replay
- signal growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature restart layer first defines the scope of reentry signals before it relies on signal quality.

---

## 6. Status

This document is the active canonical reentry-signal-scope rule until replaced by a stricter scope reference.
