# CORE DEPENDENCY DISCIPLINE v1

Status: active canonical dependency-discipline rule
Scope: structural dependency behavior across major platform layers
Rule: dependencies must follow explainable architectural direction rather than convenience-driven entanglement

---

## 1. Purpose

This document defines dependency discipline for the core platform.

It exists to prevent:
- circular architectural meaning
- hidden tight coupling
- downstream layers becoming hidden prerequisites for upstream truth
- expansion that quietly damages modularity

---

## 2. Dependency Principle

Dependencies should remain explainable in architectural terms.

Preferred logic includes:
- foundational layers support downstream layers
- downstream layers may consume upstream layers
- optional extensions must not become hidden foundational dependencies
- convenience imports must not silently redefine architecture

---

## 3. Required Rule

A dependency should be acceptable only if it fits the platform’s structural logic.

It should be possible to explain:
- why the dependency exists
- whether it is foundational or downstream
- whether it introduces structural risk

---

## 4. Forbidden Dependency Drift

The following remain forbidden:
- hidden circular dependence at architectural meaning level
- optional/mobile/extension layer becoming a hidden core prerequisite
- presentation-driven dependency reversal
- dependency choices made only for local convenience while damaging global structure

---

## 5. Final Rule

Dependency discipline protects architecture from slow entanglement.

---

## 6. Status

This document is the active canonical dependency-discipline rule until replaced by a stricter dependency architecture reference.
