# 06 PACKAGE SUMMARY READABILITY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package summaries readable to machines and humans
Rule: package summaries must remain compact, structured, and readable so future tooling can interpret package purpose without parsing the entire package body first

---

## 1. Purpose

This document defines the package-summary-readability rule of the platform.

It exists to preserve:
- readable package summaries
- lower ambiguity around package purpose
- continuity between package overview and deeper package content
- a stable base for later summary hardening

---

## 2. Summary Principle

Package summary readability should remain understandable in terms of:
- what the package is
- what it covers
- what role it plays
- what kind of followup reading is justified
- how summaries preserve navigability

---

## 3. Required Rule

Package summary readability should remain:
- explicit
- compact
- meaningful
- machine-readable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- package summaries that are too vague to interpret
- summary text that hides package role
- summary structure preserved only in style habit
- summaries that require full package reading before they become useful

---

## 5. Final Rule

A mature documentation system makes package summaries readable enough that machines and humans can orient before deep reading.

---

## 6. Status

This document is the active canonical package-summary-readability rule until replaced by a stricter summary reference.
