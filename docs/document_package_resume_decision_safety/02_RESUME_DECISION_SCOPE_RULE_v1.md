# 02 RESUME DECISION SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for how decision resumption should be bounded and interpreted across documentation packages
Rule: resume-decision scope must remain explicit so safe continuation of package decision flow stays bounded, meaningful, and usable in real maintenance work

---

## 1. Purpose

This document defines the resume-decision-scope rule of the platform.

It exists to preserve:
- bounded decision-resume interpretation
- lower ambiguity around what decision signals must be resumed first
- continuity between package role and safe decision continuation
- a stable base for later decision hardening

---

## 2. Scope Principle

Resume decision scope should remain understandable in terms of:
- what decision signals must be recoverable safely
- what remains outside safe decision reentry scope
- what decision level is primary
- how scope differs across package families

---

## 3. Required Rule

Resume decision scope should remain:
- explicit
- bounded
- meaningful
- readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined decision-resume boundaries
- safe decision resumption treated as full package replay
- scope growth with no readable discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature safety layer first defines what decision context must be safely resumable before it relies on resume quality.

---

## 6. Status

This document is the active canonical resume-decision-scope rule until replaced by a stricter scope reference.
