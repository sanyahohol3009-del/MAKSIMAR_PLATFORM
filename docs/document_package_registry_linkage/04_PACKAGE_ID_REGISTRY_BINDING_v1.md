# 04 PACKAGE ID REGISTRY BINDING v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: binding rules between package identity and registry package_id usage
Rule: package identifiers must remain stable and readable across package-manifest and registry layers

---

## 1. Purpose

This document defines the package-id-registry binding of the platform.

It exists to preserve:
- stable package identity
- readable linkage across documentation layers
- lower identity ambiguity at scale
- a stable base for future manifest and registry hardening

---

## 2. Binding Principle

Package-id binding should remain understandable in terms of:
- what the package is called
- how that identity appears in the registry
- how identity remains stable over time
- how package identity avoids drift and duplication

---

## 3. Required Rule

Package-id binding should remain:
- explicit
- stable
- readable
- machine-readable
- non-duplicative

---

## 4. What Is Forbidden

The following remain forbidden:
- unstable package identifiers
- package identity guessed from folder memory only
- duplicate identity semantics across package and registry layers
- drift between package name and registry package_id meaning

---

## 5. Final Rule

A mature documentation system binds package identity once and reuses it consistently.

---

## 6. Status

This document is the active canonical package-id-registry binding until replaced by a stricter package identity reference.
