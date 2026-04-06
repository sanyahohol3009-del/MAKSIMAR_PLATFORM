# 02 DOCUMENT STATUS MODEL v1

Status: active_canonical
Document Type: canonical
Authority Level: constitutional
Interpretation Priority: strict
Scope: allowed status values for platform documentation
Rule: document status must remain constrained so active law, drafts, replaced docs, and historical docs are not confused

---

## 1. Purpose

This document defines the document-status model of the platform.

It exists to preserve:
- consistent document lifecycle interpretation
- explicit distinction between active and inactive materials
- lower ambiguity for operators and future JARVIS
- a stable base for registry and supersession behavior

---

## 2. Allowed Status Values

The current canonical status set is:

- `active_canonical`
- `draft`
- `superseded`
- `historical_only`

---

## 3. Status Meaning

### active_canonical
The document is currently valid and should be treated as active reference.

### draft
The document is not yet accepted as canon and should not override accepted documents.

### superseded
The document was once valid but has been replaced by a newer reference.

### historical_only
The document is retained for continuity or history and should not be treated as current law.

---

## 4. Required Rule

New documents should use only the canonical status set unless a stricter status model is intentionally introduced later.

---

## 5. What Is Forbidden

The following remain forbidden:
- inventing ad hoc status labels casually
- leaving status implicit
- treating draft or historical material as current law
- failing to mark replaced documents as replaced when supersession is known

---

## 6. Final Rule

A mature documentation system makes document applicability explicit.

---

## 7. Status

This document is the active canonical document-status model until replaced by a stricter lifecycle model.
