# 02 PACKAGE ID AND SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: constitutional
Interpretation Priority: strict
Scope: rules for package identity and scope declaration in documentation manifests
Rule: each documentation package must have a stable identity and readable scope so future readers do not infer package meaning from naming alone

---

## 1. Purpose

This document defines the package-id-and-scope rule of the platform.

It exists to preserve:
- stable package naming
- readable package scope
- lower ambiguity across similarly named document families
- a stable base for future package manifests and registry expansion

---

## 2. Identity Principle

Package identity and scope should remain understandable in terms of:
- what the package is called
- what domain or subdomain it governs
- what boundary separates it from neighboring packages
- what the package is not supposed to cover

A package name without scope is weaker than it appears.

---

## 3. Required Rule

Package identity and scope should remain:
- explicit
- stable
- bounded
- human-readable
- machine-readable

---

## 4. What Is Forbidden

The following remain forbidden:
- vague package identity
- packages with drifting scope
- package meaning inferred only from chat memory
- overlapping package semantics with no readable boundary

---

## 5. Final Rule

A mature documentation system names what a package is and where its scope stops.

---

## 6. Status

This document is the active canonical package-id-and-scope rule until replaced by a stricter package identity reference.
