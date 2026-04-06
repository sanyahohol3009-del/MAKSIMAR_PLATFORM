# 05 REGISTRY DEPENDENCY FIELD BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline semantics for the depends_on field in the document registry
Rule: dependency metadata must remain explicit so future JARVIS and human readers can follow document meaning through graph structure rather than guesswork

---

## 1. Purpose

This document defines the registry-dependency-field baseline of the platform.

It exists to preserve:
- readable upstream document relations
- lower ambiguity across document interpretation
- future dependency graph hardening
- a stable base for machine-readable document navigation

---

## 2. Dependency Principle

The depends_on field should remain understandable in terms of:
- what upstream documents a package relies on
- what prior law or contract frames its meaning
- what baseline should be read first
- what dependencies are most interpretively important

---

## 3. Required Rule

The depends_on field should remain:
- explicit
- selective
- meaningful
- non-exhaustive at first
- stable enough for future graph expansion

---

## 4. What Is Forbidden

The following remain forbidden:
- empty dependency semantics forever
- dependency lists that are random or bloated
- pretending a package is self-explaining when it depends on prior law
- making dependency metadata unreadable through overgrowth

---

## 5. Final Rule

A mature document registry records what a package stands on before asking others to stand on it.

---

## 6. Status

This document is the active canonical registry-dependency-field baseline until replaced by a stricter registry dependency reference.
