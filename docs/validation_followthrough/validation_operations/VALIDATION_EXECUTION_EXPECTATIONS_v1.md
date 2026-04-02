# VALIDATION EXECUTION EXPECTATIONS v1

Status: active canonical validation execution expectations
Scope: expectations around how validation should be executed in practice
Rule: validation execution should remain explicit enough that operators know what kinds of runs are expected, not merely possible

---

## 1. Purpose

This document defines expectations for validation execution in the platform.

It exists to preserve clarity about:
- what kinds of validation runs are expected
- why both narrow and broad validation matter
- how validation execution supports platform continuity

---

## 2. Execution Expectation Principle

The platform should preserve operational expectations for validation such as:
- fast checks for quick iteration
- layer checks for focused subsystem confirmation
- full-platform checks for whole-system integrity
- serial fallback where needed
- bounded or hardware-scaled parallel runs where appropriate

---

## 3. Required Rule

Validation execution should remain:
- purposeful
- proportionate to scope and risk
- consistent with documented tiers
- respectful of full-platform integrity needs

---

## 4. What Is Forbidden

The following remain forbidden:
- no shared expectation about when broader validation matters
- drifting into only local checks forever
- interpreting maximum-speed validation as the only goal
- treating full-platform validation as a rare accident

---

## 5. Final Rule

Validation expectations make engineering rhythm real and repeatable.

---

## 6. Status

This document is the active canonical validation execution expectations until replaced by a stricter validation execution reference.
