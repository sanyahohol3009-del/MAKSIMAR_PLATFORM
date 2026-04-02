# TRUST BOUNDARIES v1

Status: active canonical trust-boundary rule
Scope: trust separation across platform layers and extensions
Rule: trust must remain segmented explicitly so optional, downstream, and external layers do not silently inherit foundational authority

---

## 1. Purpose

This document defines trust boundaries across the platform.

It exists to prevent:
- trust flattening
- hidden authority inheritance
- accidental elevation of optional components
- unsafe treatment of extensions as equivalent to foundational layers

---

## 2. Trust Boundary Principle

Not all platform layers are equally trusted for the same things.

Examples of trust distinctions include:
- foundational rules vs downstream presentation
- protected core behavior vs optional external integrations
- source-backed truth vs interpreted summaries
- approval-governed actions vs passive observation

---

## 3. Required Trust Separation

The platform should preserve explicit trust separation among:
- canonical contracts and rules
- governance and safety enforcement
- runtime behavior
- observability and diagnostics
- dashboards and operator-facing views
- mobile / bridge / accelerator extensions
- future swarm or self-awareness layers

---

## 4. Required Rule

A layer may only exercise trust consistent with its role.

Reading does not imply authority.
Presentation does not imply trust elevation.
Optional extension does not imply foundational legitimacy.

---

## 5. What Is Forbidden

The following remain forbidden:
- trust by convenience
- silent inheritance of core trust by downstream layers
- treating external/mobile/accelerator attachment as automatically trusted
- mixing trusted and less-trusted responsibilities without explicit boundary

---

## 6. Final Rule

Trust must remain segmented and explainable if the platform is to stay safe.

---

## 7. Status

This document is the active canonical trust-boundary rule until replaced by a stricter trust architecture specification.
