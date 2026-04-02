# MOBILE THERMAL POWER POLICY v1

Status: active canonical mobile thermal/power rule
Scope: mobile AI execution on phone and accelerator-assisted modes
Rule: thermal and power governance must constrain AI execution before UX or device safety degrades

---

## 1. Purpose

This document defines the canonical thermal and power policy for mobile AI execution.

It exists to prevent:
- thermal runaway
- battery abuse
- UI lag caused by inference load
- unstable long-running mobile execution
- uncontrolled compute escalation under weak power conditions

---

## 2. Required Inputs

Thermal/power governance should observe, when available:

- battery level
- charging state
- thermal status
- CPU pressure
- sustained load
- backend health under load

---

## 3. Required Reactions

The system must support controlled reactions such as:

- lower sampling frequency
- lower polling frequency
- reduced analysis window
- reduced compute intensity
- switch to degraded mode
- fallback from external to local or local to safe mode where needed

---

## 4. UX Protection Rule

The mobile UI must not become unresponsive because AI execution ignores thermal or power constraints.

Responsiveness and device safety take priority over aggressive compute behavior.

---

## 5. What Is Forbidden

The following remain forbidden:

- ignoring thermal state
- ignoring low-power conditions
- treating mobile hardware as infinite compute
- forcing full-speed inference when the device is degrading

---

## 6. Final Rule

Mobile intelligence must scale down gracefully under pressure rather than damage usability or stability.

---

## 7. Status

This document is the active canonical mobile thermal/power policy until replaced by a stricter mobile runtime governance standard.
