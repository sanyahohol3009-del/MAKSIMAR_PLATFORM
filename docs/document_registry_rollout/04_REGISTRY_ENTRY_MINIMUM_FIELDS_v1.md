# 04 REGISTRY ENTRY MINIMUM FIELDS v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: minimum required fields for new registry entries during rollout
Rule: registry rollout entries must satisfy a minimum metadata floor so coverage growth remains useful to humans and machines

---

## 1. Purpose

This document defines the registry-entry-minimum-fields baseline of the platform.

It exists to preserve:
- consistent entry quality
- lower metadata ambiguity
- machine-readable usefulness
- a stable base for future richer registry semantics

---

## 2. Minimum Field Principle

Each new registry entry should minimally include:
- doc_id or package_id
- title
- path
- status
- document_type
- authority_level
- interpretation_priority

Recommended when available:
- depends_on
- used_by
- canonical
- audit_closure
- continuity_history

---

## 3. Required Rule

Registry entry minimums should remain:
- explicit
- small enough to sustain rollout
- strong enough to preserve meaning
- consistent with document meta-governance

---

## 4. What Is Forbidden

The following remain forbidden:
- adding entries with no role metadata
- wildly different field semantics across packages
- blocking rollout on perfect completeness
- pretending a path alone is a meaningful registry entry

---

## 5. Final Rule

A mature registry grows from a stable minimum metadata floor, not from filenames alone.

---

## 6. Status

This document is the active canonical registry-entry-minimum-fields baseline until replaced by a stricter registry entry standard.
