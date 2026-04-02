# STEP EXECUTION AND DOCUMENTATION PROTOCOL v1

Status: active canonical step protocol
Scope: how project work is executed and documented
Rule: major project steps must follow a documentation-aware execution protocol

---

## 1. Purpose

This document defines the canonical protocol for executing work steps in the project.

It exists to prevent:
- coding first and explaining later
- undocumented architectural drift
- losing rationale for implementation decisions
- fragmented continuity across long project phases

---

## 2. Canonical Step Protocol

The preferred step protocol is:

1. define or update rule/documentation if needed
2. implement
3. test
4. verify outputs
5. update related documentation
6. commit/version the result

---

## 3. Required Rule

Major project work must not skip documentation when:
- a new layer appears
- a boundary changes
- a validation rule changes
- an operator-facing behavior changes
- a critical integration path is introduced

---

## 4. Lightweight vs Heavy Steps

Small local edits may not require a new standalone document every time.

However, substantial steps require documentation-aware handling.

---

## 5. What Is Forbidden

The following remain forbidden:
- repeated major steps with no documentation trail
- architecture-changing implementation with no written rationale
- relying only on chat memory for multi-step execution continuity

---

## 6. Final Rule

The project advances by documented steps, not by code alone.

---

## 7. Status

This document is the active canonical step protocol until replaced by a stricter project execution governance standard.
