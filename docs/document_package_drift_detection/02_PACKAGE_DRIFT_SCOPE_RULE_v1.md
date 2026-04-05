# 02 PACKAGE DRIFT SCOPE RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: scope rule for what package surfaces should be covered by drift detection
Rule: package-drift scope must remain explicit so drift work stays bounded, readable, and meaningful

---

## 1. Purpose

This document defines the package-drift-scope rule of the platform.

It exists to preserve:
- bounded drift detection
- lower ambiguity around what must be watched
- continuity between drift effort and real package meaning
- a stable base for later drift growth

---

## 2. Scope Principle

Package-drift scope should remain understandable in terms of:
- what package surfaces are monitored
- what fields are checked for deviation
- what may remain outside early drift scope
- what is critical enough to watch first

---

## 3. Required Rule

Package-drift scope should remain:
- explicit
- bounded
- meaningful
- incremental
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- undefined drift scope
- pretending every surface must be watched equally on day one
- drift growth with no priority discipline
- scope ambiguity preserved only in operator memory

---

## 5. Final Rule

A mature drift layer first defines what it watches before it claims useful detection.

---

## 6. Status

This document is the active canonical package-drift-scope rule until replaced by a stricter scope reference.
