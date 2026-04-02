# TEST WORKER SHUTDOWN RULE v1

Status: active canonical test worker shutdown rule
Scope: pytest-xdist workers and future parallel test worker processes
Rule: test workers must terminate cleanly, and orphaned workers must be detected and cleaned up through a controlled shutdown policy

---

## 1. Purpose

This document defines the canonical worker shutdown rule for parallel test execution.

It exists to prevent:
- orphaned pytest workers
- zombie-like test processes
- runaway CPU usage after test completion
- confusion between finished test suite and still-running workers

---

## 2. Core Principle

When a test run completes:
- workers should exit
- worker resources should be released
- no orphaned test workers should remain active

A finished test suite with still-running workers is treated as an execution hygiene defect.

---

## 3. Required Shutdown Order

The preferred shutdown order is:

1. natural worker exit
2. graceful termination
3. forced termination only if graceful termination fails

---

## 4. Graceful First Policy

Preferred cleanup commands should target pytest-related workers first with graceful termination.

Forced kill is allowed only as fallback.

The project must not normalize immediate hard-kill behavior as the default.

---

## 5. Required Detection Principle

After a parallel run, the operator should be able to determine:
- whether workers exited
- whether workers are stuck
- whether processes belong to pytest or to unrelated Python activity

Worker cleanup must not blindly kill unrelated Python processes.

---

## 6. Required Future Hardening

The platform should later support:
- worker shutdown timeout policy
- orphan worker detection
- post-run cleanup verification
- observability for test worker lifecycle
- incident logging for shutdown failures

---

## 7. What Is Forbidden

The following remain forbidden:
- treating orphaned workers as normal
- blind hard-kill of all Python processes as default habit
- no distinction between graceful stop and forced stop
- ignoring residual worker processes after successful test completion

---

## 8. Final Rule

Test workers must exit cleanly whenever possible.
Forced cleanup is a fallback, not a default operating mode.

---

## 9. Status

This document is the active canonical test worker shutdown rule until replaced by a stricter worker lifecycle governance standard.
