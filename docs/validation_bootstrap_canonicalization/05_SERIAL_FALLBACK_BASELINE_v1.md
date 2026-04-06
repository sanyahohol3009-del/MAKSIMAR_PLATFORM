# 05 SERIAL FALLBACK BASELINE v1

Status: active canonical serial-fallback baseline
Scope: correctness-preserving fallback when parallel or alternate launch modes are ambiguous
Rule: serial fallback must remain available so validation interpretation does not depend on one execution style only

---

## 1. Purpose

This document defines the serial-fallback baseline of the platform.

It exists to preserve:
- correctness-first validation fallback
- readable interpretation when launch modes differ
- stable diagnosis path for parallel uncertainty
- a base for later validation hardening procedures

---

## 2. Serial Principle

Serial fallback should remain understandable in terms of:
- simpler execution interpretation
- reduced concurrency ambiguity
- stronger diagnosis value when parallel behavior is questionable
- preservation of validation trust

---

## 3. Current Confirmed Fallback

Current strong fallback entrypoint:
- `python -m pytest -q`

This is currently confirmed to pass the full suite.

---

## 4. What Is Forbidden

The following remain forbidden:
- abandoning serial fallback entirely
- treating fallback as unnecessary because parallel works today
- losing a correctness-first reference mode
- letting validation meaning depend on one fast path only

---

## 5. Final Rule

A serious platform preserves a slower but cleaner fallback path.

---

## 6. Status

This document is the active canonical serial-fallback baseline until replaced by a stricter validation fallback reference.
