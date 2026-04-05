# 06 REGISTRY ALIGNMENT REPAIR RUNBOOK v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: runbook for repairing package alignment with the central document registry
Rule: package/registry alignment issues should be repaired through a readable sequence so package meaning and registry meaning remain mutually trustworthy

---

## 1. Purpose

This document defines the registry-alignment-repair runbook of the platform.

It exists to preserve:
- readable cross-layer repair
- lower risk of package/registry contradiction
- continuity between manifest and registry meaning
- a stable base for later sync hardening

---

## 2. Repair Principle

Registry-alignment repair should remain understandable in terms of:
- what field or layer drifted
- what alignment broke
- what should be corrected first
- how repair restores trustworthy cross-layer meaning

---

## 3. Required Rule

Registry-alignment repair should remain:
- explicit
- machine-readable
- non-contradictory
- incrementally hardenable
- canon-preserving

---

## 4. What Is Forbidden

The following remain forbidden:
- package and registry layers diverging silently after repair work
- cross-layer contradiction treated as harmless
- repair guessed only from memory
- package trust claims with no registry discipline

---

## 5. Final Rule

A mature documentation system repairs registry alignment as part of package quality, not as a separate afterthought.

---

## 6. Status

This document is the active canonical registry-alignment-repair runbook until replaced by a stricter alignment repair reference.
