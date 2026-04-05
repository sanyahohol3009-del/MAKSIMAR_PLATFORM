# 03 PACKAGE METADATA READABILITY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package metadata machine-readable and meaningful
Rule: package metadata must remain machine-readable so package identity, status, authority, and linkage can be interpreted consistently by future tooling

---

## 1. Purpose

This document defines the package-metadata-readability rule of the platform.

It exists to preserve:
- readable structured metadata
- lower ambiguity around package identity fields
- continuity between package meaning and machine-readable metadata
- a stable base for later machine-readability hardening

---

## 2. Metadata Principle

Package metadata readability should remain understandable in terms of:
- what fields have stable meaning
- what values remain normalized
- what metadata supports navigation and interpretation
- how metadata preserves documentation trust

---

## 3. Required Rule

Package metadata readability should remain:
- explicit
- stable
- meaningful
- machine-readable
- non-decorative

---

## 4. What Is Forbidden

The following remain forbidden:
- unstable metadata meaning
- decorative structured fields
- metadata that changes semantics from package to package
- machine-readable meaning preserved only in operator memory

---

## 5. Final Rule

A mature documentation system keeps package metadata readable to machines because identity and governance depend on it.

---

## 6. Status

This document is the active canonical package-metadata-readability rule until replaced by a stricter metadata reference.
