# 06 PACKAGE USED BY CAPTURE DISCIPLINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: practical discipline for capturing package-level used_by metadata during rollout
Rule: package downstream usage capture must remain selective and meaningful so rollout builds a readable package graph in both directions

---

## 1. Purpose

This document defines the package-used-by-capture discipline of the platform.

It exists to preserve:
- useful downstream package references
- lower ambiguity about future package reliance
- gradual bidirectional graph growth
- a stable base for later graph hardening

---

## 2. Capture Principle

Package used_by capture should remain understandable in terms of:
- what future package may rely on the current one
- what downstream relevance exists
- what future manifest or registry surface this package supports
- what references may remain omitted for now without harming readability

---

## 3. Required Rule

Package used_by capture should remain:
- explicit
- selective
- meaningful
- incremental
- non-bloated

---

## 4. What Is Forbidden

The following remain forbidden:
- downstream meaning preserved only in chat memory
- speculative giant used_by lists
- decorative downstream metadata with no interpretive role
- pretending package meaning ends at its own folder

---

## 5. Final Rule

A mature package graph records not only upstream dependency, but downstream relevance.

---

## 6. Status

This document is the active canonical package-used-by-capture discipline until replaced by a stricter downstream package graph reference.
