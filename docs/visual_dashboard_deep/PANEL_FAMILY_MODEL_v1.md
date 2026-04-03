# PANEL FAMILY MODEL v1

Status: active canonical panel-family model
Scope: grouping dashboard panels into semantic families
Rule: panels should be grouped into readable families so dashboard structure remains explainable as the system grows

---

## 1. Purpose

This document defines the panel-family model of the platform.

It exists to preserve clarity about:
- why panels should belong to families
- how family grouping reduces dashboard sprawl
- why panel growth must remain semantically organized

---

## 2. Family Principle

Panels may belong to families such as:
- runtime status
- health and degraded state
- diagnostics and incident context
- navigation and overview
- future visual or topology-oriented families

These families are semantic groupings, not mere layout tricks.

---

## 3. Required Rule

Panel family interpretation should remain explainable in terms of:
- semantic purpose
- operator concern
- upstream meaning dependency
- bounded relation to other panel families

---

## 4. What Is Forbidden

The following remain forbidden:
- every panel treated as isolated visual furniture
- family identity inferred only by screen position
- panel growth with no grouping discipline
- family labels used as decorative naming with no semantic consequence

---

## 5. Final Rule

Panel families make dashboard growth readable when they remain semantic rather than cosmetic.

---

## 6. Status

This document is the active canonical panel-family model until replaced by a stricter dashboard-family reference.
