# 02 REPO ROOT GUARD BASELINE v1

Status: active canonical repo-root-guard baseline
Scope: guarding validation against launch from the wrong directory
Rule: validation should be guarded against wrong-root execution so collection and import interpretation remain trustworthy

---

## 1. Purpose

This document defines the repo-root-guard baseline of the platform.

It exists to preserve:
- correct working-directory discipline
- reduced bootstrap ambiguity
- explicit protection against off-root validation launches
- a stable base for later wrapper and CI guardrails

---

## 2. Repo-Root Principle

Repo-root guarding should remain understandable in terms of:
- expected project root
- expected command location
- prevention of accidental off-root execution
- protection of import and collection interpretation

---

## 3. Required Rule

Repo-root guarding should remain:
- explicit
- lightweight
- trustworthy
- validation-oriented
- subordinate to canonical bootstrap policy

---

## 4. What Is Forbidden

The following remain forbidden:
- running whole-suite validation from arbitrary subdirectories
- trusting accidental shell location
- ignoring wrong-root launch risk
- hiding root assumptions in tribal knowledge

---

## 5. Final Rule

A serious validation system should know whether it was launched from the right root.

---

## 6. Status

This document is the active canonical repo-root-guard baseline until replaced by a stricter repo-root enforcement reference.
