# 04 PARALLEL VALIDATION EXECUTION BASELINE v1

Status: active canonical parallel-validation-execution baseline
Scope: bounded use of parallel pytest execution for whole-suite validation
Rule: parallel validation must remain explicitly interpreted so speed gains do not silently replace correctness discipline

---

## 1. Purpose

This document defines the parallel-validation-execution baseline of the platform.

It exists to preserve:
- explicit use of multi-core validation
- bounded interpretation of xdist-based execution
- distinction between performance and correctness
- a stable base for later CI/CD scaling

---

## 2. Parallel Principle

Parallel validation should remain understandable in terms of:
- speed improvement
- worker isolation risk
- possible race or flakiness exposure
- need for fallback serial execution when interpretation is uncertain

Parallel success is valuable, but not sufficient alone.

---

## 3. Current Confirmed Interpretation

The repository has a confirmed passing parallel full-suite run with:

- `PYTHONPATH="$PWD" pytest -q -n auto`

This is currently the preferred fast whole-suite path.

---

## 4. What Is Forbidden

The following remain forbidden:
- treating fast parallel green as the only required proof
- forgetting serial fallback discipline
- ignoring race-risk in shared-state tests
- assuming parallelism is neutral in all suites

---

## 5. Final Rule

A mature validation system uses parallelism intentionally, not blindly.

---

## 6. Status

This document is the active canonical parallel-validation-execution baseline until replaced by a stricter validation execution reference.
