# 03 DOCUMENT TYPE AND AUTHORITY MODEL v1

Status: active_canonical
Document Type: canonical
Authority Level: constitutional
Interpretation Priority: strict
Scope: document role classes and authority interpretation across the documentation universe
Rule: document type and authority must remain explicit so law, contracts, audits, and history are not flattened into one undifferentiated layer

---

## 1. Purpose

This document defines the document-type and authority model of the platform.

It exists to preserve:
- clear distinction among law, contracts, audits, and history
- readable authority interpretation
- machine-readable governance memory
- a stable base for future self-reading document systems

---

## 2. Canonical Document Types

The current canonical document-type set is:

- `canonical`
- `audit_closure`
- `continuity_history`
- `draft`

---

## 3. Authority Levels

The current authority-level set is:

- `constitutional`
- `operational`
- `reference`
- `historical`

---

## 4. Interpretation Principle

Document type and authority should be interpreted together.

Examples:
- canonical + constitutional = law-like governing material
- canonical + operational = active working contract or layer guidance
- audit_closure + reference = closure and completion context
- continuity_history + historical = continuity memory, not active law

---

## 5. Required Rule

New documents should declare both document type and authority level explicitly.

---

## 6. What Is Forbidden

The following remain forbidden:
- treating every markdown file as equally authoritative
- mixing closure notes with laws under one flat interpretation
- using history as if it were active constitutional guidance
- omitting authority semantics in new documentation

---

## 7. Final Rule

A mature platform distinguishes what governs it from what merely describes its past.

---

## 8. Status

This document is the active canonical document-type and authority model until replaced by a stricter document-governance standard.
