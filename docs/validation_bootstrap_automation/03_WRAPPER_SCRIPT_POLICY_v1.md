# 03 WRAPPER SCRIPT POLICY v1

Status: active canonical wrapper-script policy
Scope: wrapper-based launch discipline for validation bootstrap
Rule: wrapper scripts must remain explicit and trustworthy so they reduce ambiguity instead of introducing hidden launch behavior

---

## 1. Purpose

This document defines the wrapper-script policy of the platform.

It exists to preserve:
- readable wrapper behavior
- trusted validation entrypoints
- bounded automation semantics
- continuity between manual and automated launch modes

---

## 2. Wrapper Principle

A wrapper script should remain understandable in terms of:
- what environment it assumes
- what root it expects
- what command it runs
- what it validates before launch
- what fallback behavior it preserves

A wrapper must not become a black box.

---

## 3. Required Rule

Wrapper-script policy should remain:
- explicit
- inspectable
- bootstrap-aware
- fallback-aware
- compatible with canonical validation commands

---

## 4. What Is Forbidden

The following remain forbidden:
- wrapper scripts with hidden path mutation
- silent environment switching
- unclear interpreter selection
- convenience wrappers that obscure correctness interpretation

---

## 5. Final Rule

A mature platform may use wrappers, but those wrappers must remain readable and trustworthy.

---

## 6. Status

This document is the active canonical wrapper-script policy until replaced by a stricter validation wrapper reference.
