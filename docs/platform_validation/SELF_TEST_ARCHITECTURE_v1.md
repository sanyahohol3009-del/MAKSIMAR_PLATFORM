# SELF TEST ARCHITECTURE v1

Status: active canonical self-test architecture rule
Scope: code validation, runtime validation, bounded automated checks
Rule: the platform may verify itself automatically, but self-testing must remain bounded, observable, and non-authoritative over immutable truth

---

## 1. Purpose

This document defines the canonical self-test architecture for MAKSIMAR/JARVIS.

It exists to ensure that the platform can:
- run automated checks
- validate code and runtime health
- detect regressions early
- reduce manual operator burden

without allowing:
- uncontrolled recursive testing
- self-test overload
- self-test ownership of truth
- hidden mutation through validation paths

---

## 2. Core Principle

Self-testing is a platform verification capability.

It must remain:
- bounded
- scheduled or triggered
- observable
- non-authoritative over source-of-truth
- safe to disable or degrade

---

## 3. What Self-Test May Cover

The self-test layer may validate:
- Python compilation
- smoke tests
- selected layer tests
- full test suite
- runtime state consistency
- guard-chain health
- document presence/consistency
- future architectural invariants

---

## 4. What Self-Test Must Not Become

The self-test layer is not:
- immutable core
- policy authority
- execution control
- deployment authority
- proof that everything in the system is correct forever

---

## 5. Final Rule

The system may test itself automatically,
but self-testing must remain a bounded verification layer, not a second brain.

---

## 6. Status

This document is the active canonical self-test architecture rule until replaced by a stricter platform verification standard.
