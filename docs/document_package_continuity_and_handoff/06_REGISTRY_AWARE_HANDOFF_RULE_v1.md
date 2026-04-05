# 06 REGISTRY AWARE HANDOFF RULE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: rule for keeping package handoff aligned with the central document registry
Rule: package handoff must remain registry-aware so transferred package state does not drift away from declared package metadata and status

---

## 1. Purpose

This document defines the registry-aware-handoff rule of the platform.

It exists to preserve:
- readable package-to-registry continuity
- lower ambiguity across handoff and registry layers
- continuity between transferred package state and machine-readable metadata
- a stable base for later continuity hardening

---

## 2. Registry Principle

Registry-aware handoff should remain understandable in terms of:
- what handoff fields align with registry fields
- what package state remains interoperable
- how handoff preserves navigation trust
- how state drift is avoided

---

## 3. Required Rule

Registry-aware handoff should remain:
- explicit
- machine-readable
- non-contradictory
- alignment-aware
- incrementally hardenable

---

## 4. What Is Forbidden

The following remain forbidden:
- handoff that conflicts with registry meaning
- silent transfer assumptions
- registry-aware handoff guessed only from memory
- package transfer that cannot map cleanly into registry interpretation

---

## 5. Final Rule

A mature documentation system keeps package handoff aligned with the registry because continuity depends on that stability.

---

## 6. Status

This document is the active canonical registry-aware-handoff rule until replaced by a stricter continuity reference.
