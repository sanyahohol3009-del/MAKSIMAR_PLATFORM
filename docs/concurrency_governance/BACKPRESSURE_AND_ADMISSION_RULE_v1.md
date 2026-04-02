# BACKPRESSURE AND ADMISSION RULE v1

Status: active canonical pressure rule
Scope: queues, workers, task admission, overload behavior
Rule: the platform must degrade safely under pressure instead of pretending infinite capacity

---

## 1. Purpose

This document defines the canonical backpressure and admission rule.

It exists to prevent:
- overload collapse
- unbounded queue growth
- latency runaway
- fake responsiveness under pressure
- silent starvation

---

## 2. Core Principle

The platform must not assume infinite throughput.

Under load, it must:
- measure pressure
- classify pressure
- limit admission
- delay or reject low-priority work
- preserve critical paths

---

## 3. Required Controls

The platform must support:
- queue depth limits
- concurrency limits
- admission gating
- degraded mode triggers
- priority-aware scheduling
- overload observability

---

## 4. Required States

Pressure should be representable in states such as:
- nominal
- elevated
- constrained
- degraded
- overload

---

## 5. What Is Forbidden

The following remain forbidden:
- infinite queue growth by default
- accepting all work blindly
- silent overload
- letting low-priority work destroy critical paths

---

## 6. Final Rule

Responsiveness under pressure is achieved through control, not optimism.

---

## 7. Status

This document is the active canonical backpressure and admission rule until replaced by a stricter pressure governance standard.
