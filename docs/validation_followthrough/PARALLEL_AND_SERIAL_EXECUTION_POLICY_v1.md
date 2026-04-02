# PARALLEL AND SERIAL EXECUTION POLICY v1

Status: active canonical serial/parallel validation policy
Scope: relationship between serial and parallel validation modes
Rule: the platform must preserve both serial correctness fallback and bounded or hardware-scaled parallel validation as legitimate execution profiles

---

## 1. Purpose

This document defines the current policy for serial and parallel validation execution.

It exists to preserve clarity about:
- when serial matters
- when parallel matters
- why one does not fully replace the other

---

## 2. Policy Principle

Serial execution remains:
- correctness fallback
- debugging fallback
- isolation-sensitive fallback

Parallel execution remains:
- performance-oriented validation mode
- broader hardware utilization mode
- useful detector of isolation and contention defects

Both matter.

---

## 3. Required Rule

The platform should preserve at least:
- serial validation path
- bounded parallel path
- hardware-scaled parallel path where safe

The project must not collapse all validation thinking into one execution profile only.

---

## 4. Interpretation Rule

A green serial run is valuable.
A green parallel run is valuable.
They do not always prove exactly the same thing.

The platform should preserve this interpretive discipline.

---

## 5. What Is Forbidden

The following remain forbidden:
- assuming serial alone proves everything
- assuming parallel alone proves everything
- deleting serial fallback discipline
- treating parallel-only failures as uninterpretable noise

---

## 6. Final Rule

Serial protects correctness fallback.
Parallel protects throughput and reveals different classes of defects.
Both are part of mature validation.

---

## 7. Status

This document is the active canonical serial/parallel validation policy until replaced by a stricter validation execution reference.
