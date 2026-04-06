# 04 MAKEFILE BINDING BASELINE v1

Status: active canonical Makefile-binding baseline
Scope: binding canonical validation bootstrap into Makefile-oriented developer workflow
Rule: Makefile binding must remain aligned with canonical validation bootstrap so convenience commands do not drift away from trusted execution paths

---

## 1. Purpose

This document defines the Makefile-binding baseline of the platform.

It exists to preserve:
- alignment between canonical validation rules and local developer shortcuts
- repeatable launch semantics
- lower drift between docs and real commands
- a stable base for later tooling integration

---

## 2. Makefile Principle

Makefile binding should remain understandable in terms of:
- what target invokes which validation mode
- whether repo-root and interpreter assumptions are preserved
- whether fast and fallback modes remain distinguishable
- whether convenience stays subordinate to correctness

---

## 3. Required Rule

Makefile binding should remain:
- explicit
- doc-aligned
- reproducible
- validation-aware
- non-magical

---

## 4. What Is Forbidden

The following remain forbidden:
- Makefile shortcuts that silently change validation meaning
- convenience targets detached from canonical entrypoints
- undocumented validation targets
- Makefile drift away from trusted launch discipline

---

## 5. Final Rule

Convenience is acceptable only when it preserves canonical validation meaning.

---

## 6. Status

This document is the active canonical Makefile-binding baseline until replaced by a stricter tooling-binding reference.
