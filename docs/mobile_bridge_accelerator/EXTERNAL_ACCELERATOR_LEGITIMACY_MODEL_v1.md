# EXTERNAL ACCELERATOR LEGITIMACY MODEL v1

Status: active canonical external-accelerator legitimacy model
Scope: how external accelerator hardware should be interpreted by the platform
Rule: an external accelerator must remain an optional capability extension and must not silently redefine the legitimacy of the base platform

---

## 1. Purpose

This document defines the legitimacy model for external accelerator use in the platform.

It exists to preserve clarity about:
- why an accelerator is useful
- why an accelerator is not the source of platform identity
- how extension hardware fits without becoming hidden architectural coercion

---

## 2. Legitimacy Principle

The base platform should remain valid in:
- phone-only mode
- phone plus accelerator mode
- phone plus home-node mode
- broader future extension ecosystems

The external accelerator strengthens capability.
It does not create the platform’s right to exist.

---

## 3. Required Rule

An external accelerator should remain:
- optional
- bounded
- bridge-mediated
- non-authoritative over base legitimacy
- explainable as extension rather than foundation

---

## 4. What Is Forbidden

The following remain forbidden:
- treating the accelerator as the only real system mode
- making extension hardware the hidden platform root
- allowing external attachment to redefine foundational platform discipline
- framing fallback to non-accelerated modes as illegitimate existence

---

## 5. Final Rule

An accelerator is a capability upgrade, not a legitimacy source.

---

## 6. Status

This document is the active canonical external-accelerator legitimacy model until replaced by a stricter accelerator integration reference.
