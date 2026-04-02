# BOOT AND SHUTDOWN DISCIPLINE v1

Status: active canonical boot/shutdown discipline
Scope: startup and stop behavior for the live platform
Rule: boot and shutdown must remain explicit, orderly, and explainable rather than operator folklore

---

## 1. Purpose

This document defines the current boot and shutdown discipline of the platform.

It exists to prevent:
- vague startup behavior
- vague shutdown behavior
- operator uncertainty during live system transitions
- hidden ordering assumptions

---

## 2. Boot Principle

Boot should be understood as an ordered transition into active runtime, not as an accidental side effect.

The boot understanding should preserve:
- startup intention
- initialization order awareness
- visibility of readiness
- visibility of guarded state

---

## 3. Shutdown Principle

Shutdown should be understood as an ordered transition out of active runtime, not as a chaotic stop event.

The shutdown understanding should preserve:
- stop intention
- orderly release of runtime activity
- explainability of final runtime state
- diagnostic continuity if something went wrong

---

## 4. Required Rule

Boot and shutdown behavior must remain:
- explicit
- bounded
- understandable
- documentable
- diagnosable

---

## 5. What Is Forbidden

The following remain forbidden:
- startup by unexplained ritual
- shutdown by operator guesswork
- hidden order dependencies with no documentation
- treating orderly stop as optional polish

---

## 6. Final Rule

A serious platform must be able to explain how it starts and how it stops.

---

## 7. Status

This document is the active canonical boot/shutdown discipline until replaced by a stricter operational lifecycle reference.
