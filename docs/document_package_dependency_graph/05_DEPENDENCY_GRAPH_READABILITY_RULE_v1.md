# 05 DEPENDENCY GRAPH READABILITY RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping the documentation dependency graph readable
Rule: the package dependency graph must remain readable so graph growth improves navigation instead of creating semantic clutter

---

## 1. Purpose

This document defines the dependency-graph-readability rule of the platform.

It exists to preserve:
- readable graph structure
- lower graph ambiguity
- continuity between graph density and graph usefulness
- a stable base for later graph hardening

---

## 2. Readability Principle

Dependency graph readability should remain understandable in terms of:
- what relations matter most
- what relations are too weak to record yet
- how graph structure stays navigable
- how readability preserves documentation trust

---

## 3. Required Rule

Dependency graph readability should remain:
- explicit
- selective
- meaningful
- navigable
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- graph growth that destroys readability
- decorative graph density
- weak relations normalized as equal to strong ones
- graph interpretation preserved only in operator memory

---

## 5. Final Rule

A mature documentation graph grows in clarity before it grows in density.

---

## 6. Status

This document is the active canonical dependency-graph-readability rule until replaced by a stricter graph reference.
