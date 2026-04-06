# 06 DEVELOPER TOOLING ALIGNMENT BASELINE v1

Status: active canonical developer-tooling-alignment baseline
Scope: alignment of developer-facing tooling with canonical validation bootstrap rules
Rule: developer tooling must remain aligned with canonical validation bootstrap so convenience does not create validation drift

---

## 1. Purpose

This document defines the developer-tooling-alignment baseline of the platform.

It exists to preserve:
- consistency between daily developer workflow and canonical validation rules
- lower risk of tool-driven validation drift
- readable relation between tooling and trusted launch modes
- a stable base for later editor, script, and automation integration

---

## 2. Tooling Principle

Developer tooling alignment should remain understandable in terms of:
- what tool launches validation
- what interpreter and root assumptions it uses
- whether it preserves canonical entrypoint meaning
- whether it introduces ambiguity into result interpretation

Tooling should support discipline, not replace it with guesswork.

---

## 3. Required Rule

Developer tooling alignment should remain:
- explicit
- validation-aware
- repo-root aware
- interpreter-aware
- subordinate to canonical validation policy

---

## 4. What Is Forbidden

The following remain forbidden:
- editor or shell tooling that silently changes validation meaning
- undocumented tool-specific launch behavior
- convenience-first drift away from canonical entrypoints
- tooling assumptions preserved only in memory

---

## 5. Final Rule

A mature platform aligns developer tooling with trusted validation behavior instead of letting tools invent their own rules.

---

## 6. Status

This document is the active canonical developer-tooling-alignment baseline until replaced by a stricter tooling-integration reference.
