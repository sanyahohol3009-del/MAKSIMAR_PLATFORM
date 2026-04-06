# 01 DOCUMENT HEADER STANDARD v1

Status: active_canonical
Document Type: canonical
Authority Level: constitutional
Interpretation Priority: strict
Scope: standard header fields for new documentation across the platform
Rule: new documents must start with a standard header so human and machine readers can interpret document role before reading the body

---

## 1. Purpose

This document defines the standard header for new platform documents.

It exists to preserve:
- immediate document-role readability
- consistent machine-readable interpretation
- lower ambiguity across growing documentation families
- a stable base for future registry and self-reading behavior

---

## 2. Required Header Fields

All new canonical documentation should include the following header fields:

- Status
- Document Type
- Authority Level
- Interpretation Priority
- Scope
- Rule

Recommended future-compatible fields:
- Supersedes
- Depends On
- Used By

---

## 3. Header Principle

A document header should make clear:
- whether the document is active or historical
- whether it is law, contract, audit, or continuity material
- how strongly it should be interpreted
- what scope it governs
- what rule it establishes

The reader should not have to infer document authority from style alone.

---

## 4. Required Rule

New documents should adopt the standard header immediately.

Older documents may be normalized gradually rather than rewritten all at once.

---

## 5. What Is Forbidden

The following remain forbidden:
- adding new documents with no readable authority metadata
- forcing humans or future JARVIS to guess document role from filename alone
- mixing historical and canonical documents under identical interpretation weight
- uncontrolled header drift across new documentation passes

---

## 6. Final Rule

A mature documentation system identifies document role before document content.

---

## 7. Status

This document is the active canonical document-header standard until replaced by a stricter documentation metadata standard.
