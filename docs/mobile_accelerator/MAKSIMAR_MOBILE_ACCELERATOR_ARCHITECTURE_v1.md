# MAKSIMAR MOBILE ACCELERATOR ARCHITECTURE v1

Status: active canonical mobile accelerator architecture rule
Scope: mobile app shell, local mobile AI core, external accelerator case, home-node extension
Rule: the mobile accelerator extends platform capability but must not become a hard dependency of the base platform

---

## 1. Purpose

This document defines the architectural place of the MAKSIMAR mobile accelerator concept.

It exists to ensure that:
- the mobile application remains valid without an accelerator
- an external accelerator case can extend compute capability cleanly
- the platform can scale from phone-only mode to richer hardware-assisted modes
- the architecture remains modular and bridge-driven

---

## 2. Core Principle

The mobile accelerator is an extension layer, not a legitimacy layer.

The base platform must remain functional in:

- phone-only mode
- phone + accelerator case mode
- phone + home node mode
- phone + home node + external modules mode

The external accelerator must improve capability,
but must not define whether the platform exists.

---

## 3. Canonical Layering

The preferred split is:

- Mobile App Shell
- AI Bridge Layer
- Local Mobile AI Backend
- External Accelerator Adapter
- Home/Remote Node Backend
- Policy / Thermal / Power Governance

---

## 4. Required Rule

The mobile app must not directly bind UI logic to a specific backend.

For the app layer, the AI subsystem must always look like one bridge-driven capability surface.

---

## 5. What Is Forbidden

The following remain forbidden:

- accelerator-only platform legitimacy
- direct UI dependence on one backend implementation
- mixing transport logic into UI shell
- mixing thermal policy into view code
- treating the accelerator case as a mandatory workaround

---

## 6. Final Rule

The mobile accelerator is a modular compute extension.
The platform must remain valid with or without it.

---

## 7. Status

This document is the active canonical mobile accelerator architecture rule until replaced by a stricter mobile hardware extension standard.
