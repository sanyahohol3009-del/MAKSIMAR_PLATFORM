# DOCUMENTATION ARCHITECTURE v1

Status: active canonical documentation architecture rule
Scope: full-project documentation system
Rule: documentation is a first-class system layer and must be treated as part of platform architecture, not as optional commentary

---

## 1. Purpose

This document defines the architectural role of documentation in MAKSIMAR/JARVIS.

It exists to ensure that:
- architecture remains understandable over time
- operators can recover context reliably
- implementation boundaries remain visible
- continuity is preserved across chats, sessions, and future contributors
- system behavior is explainable, not only executable

---

## 2. Core Principle

Documentation is part of the platform.

It is not:
- decoration
- afterthought
- optional polish
- disposable note-taking

It is:
- architectural memory
- operator memory
- governance memory
- validation memory
- continuity memory

---

## 3. Architectural Position

Documentation must sit alongside the platform as a canonical layer supporting:

- architecture
- runtime
- security
- validation
- observability
- incidents
- visual/dashboard logic
- mobile/bridge logic
- future self-awareness and swarm logic

---

## 4. Documentation and Truth

Documentation does not replace runtime truth, but it defines:
- what the truth sources are
- how they are interpreted
- which rules govern them
- which behaviors are allowed or forbidden

---

## 5. Required Rule

Every major project layer must have explicit documentation sufficient to preserve:
- purpose
- boundaries
- invariants
- expected inputs/outputs
- failure behavior
- operator understanding

---

## 6. What Is Forbidden

The following remain forbidden:
- undocumented critical architecture
- undocumented safety assumptions
- undocumented integration boundaries
- relying on memory alone for system-defining behavior

---

## 7. Final Rule

The project is not fully built unless it is also documented.

---

## 8. Status

This document is the active canonical documentation architecture rule until replaced by a stricter documentation governance standard.
