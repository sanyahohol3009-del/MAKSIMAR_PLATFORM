# EXTERNAL ACCELERATOR DISCOVERY HANDSHAKE v1

Status: active canonical discovery/handshake rule
Scope: external accelerator detection and validation
Rule: the app may switch to external accelerator mode only after complete discovery and validated handshake

---

## 1. Purpose

This document defines the canonical discovery and handshake rule for the external accelerator.

It exists to prevent:
- blind backend switching
- false-positive device matches
- unsafe external routing
- capability ambiguity

---

## 2. Discovery Principle

The platform may probe external accelerator presence through transports such as:

- USB-C
- Bluetooth control path
- future wired hardware extension interfaces

Transport choice must not bypass capability verification.

---

## 3. Validation Requirements

An external accelerator is considered valid only if all required identity checks pass, including:

- device identifier
- protocol version
- capability profile
- connection state
- handshake completion

---

## 4. Required Backend Switch Rule

The backend must not switch to external mode unless handshake is complete and validated.

Partial discovery is not sufficient.
Transport presence alone is not sufficient.

---

## 5. Failure Behavior

If discovery or handshake fails:
- remain in local mode
- or remain in current safe mode
- expose failure through health/diagnostic state
- do not silently claim accelerator availability

---

## 6. What Is Forbidden

The following remain forbidden:

- backend switch on incomplete identity
- backend switch on incomplete protocol match
- silent acceptance of unknown devices
- trusting transport presence as proof of capability

---

## 7. Final Rule

Discovery finds candidates.
Handshake validates candidates.
Only validated candidates may become active backends.

---

## 8. Status

This document is the active canonical discovery and handshake rule until replaced by a stricter external compute attachment standard.
