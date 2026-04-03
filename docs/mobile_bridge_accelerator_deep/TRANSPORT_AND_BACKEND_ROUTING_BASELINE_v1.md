# TRANSPORT AND BACKEND ROUTING BASELINE v1

Status: active canonical transport/backend-routing baseline
Scope: transport surfaces and backend routing behavior across local and external execution paths
Rule: transport and backend routing must remain explicit so execution-path changes are controlled and explainable

---

## 1. Purpose

This document defines the transport and backend-routing baseline of the platform.

It exists to preserve:
- readable routing between app, bridge, and backend
- bounded transport semantics
- stable distinction between local and external execution paths
- a stable base for later transport and routing families

---

## 2. Transport Principle

Transport should remain understandable in terms of:
- how data moves between bridge and backend
- what path is local versus external
- what communication surface is used
- what instability or limitation may affect continuity

Transport is not app semantics.
It is execution-path plumbing with architectural meaning.

---

## 3. Backend Routing Principle

Backend routing should remain understandable in terms of:
- which backend is active
- why that backend was selected
- what fallback path exists
- what continuity must survive path changes

Routing is not legitimacy by itself.
Routing is governed path selection.

---

## 4. Required Rule

Transport and backend routing interpretation should remain:
- explicit
- bounded
- continuity-aware
- distinct from app meaning
- consistent with fallback, thermal, and governance documentation

---

## 5. What Is Forbidden

The following remain forbidden:
- routing logic hidden behind vague app behavior
- transport instability treated as invisible architecture
- backend path changes with no readable model
- routing treated as self-justifying authority

---

## 6. Final Rule

A mature mobile execution layer must make transport and routing understandable, not magical.

---

## 7. Status

This document is the active canonical transport/backend-routing baseline until replaced by a stricter routing reference.
