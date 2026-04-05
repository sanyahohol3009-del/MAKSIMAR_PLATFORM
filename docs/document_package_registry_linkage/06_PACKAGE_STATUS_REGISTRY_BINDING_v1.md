# 06 PACKAGE STATUS REGISTRY BINDING v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: binding rules between package status interpretation and registry status metadata
Rule: package status must remain aligned across package and registry layers so interpretation priority is not weakened by status drift

---

## 1. Purpose

This document defines the package-status-registry binding of the platform.

It exists to preserve:
- readable package applicability
- lower ambiguity across active, historical, or draft interpretation
- continuity between package meaning and registry meaning
- a stable base for future status hardening

---

## 2. Binding Principle

Package-status binding should remain understandable in terms of:
- whether a package is active
- whether it is draft, superseded, or historical
- how that status appears in the registry
- how status meaning remains trustworthy across layers

---

## 3. Required Rule

Package-status binding should remain:
- explicit
- aligned
- machine-readable
- interpretation-aware
- stable

---

## 4. What Is Forbidden

The following remain forbidden:
- package status that differs from registry status
- hidden applicability drift
- status meaning inferred only from filename or age
- weakening interpretive trust through status inconsistency

---

## 5. Final Rule

A mature documentation system keeps package status aligned wherever it is represented.

---

## 6. Status

This document is the active canonical package-status-registry binding until replaced by a stricter status binding reference.
