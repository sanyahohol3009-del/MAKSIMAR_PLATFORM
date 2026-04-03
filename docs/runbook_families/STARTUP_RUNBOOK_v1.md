# STARTUP RUNBOOK v1

Status: active canonical startup runbook
Scope: operator-facing startup procedure for the platform
Rule: startup must follow an explicit, readable, and bounded procedure rather than habit or guesswork

---

## 1. Purpose

This document defines the canonical startup runbook of the platform.

It exists to preserve:
- repeatable boot behavior
- operator startup discipline
- explainable readiness thinking
- continuity between runtime architecture and practical execution

---

## 2. Startup Intent

Startup is not merely “launch things.”

Startup should preserve:
- explicit operator intent
- ordered transition into active runtime
- visibility of readiness
- visibility of abnormal startup conditions

---

## 3. Canonical Startup Procedure

The operator should conceptually follow this order:

1. confirm the correct project environment
2. confirm required runtime context is available
3. initiate startup through the project’s canonical startup path
4. observe whether runtime enters expected startup and active phases
5. confirm no obvious degraded or incident condition appears during startup

---

## 4. Required Rule

Startup procedure should remain:
- explicit
- bounded
- observable
- consistent with runtime lifecycle documentation
- diagnosable when it fails

---

## 5. What Is Forbidden

The following remain forbidden:
- startup by memory only
- startup by undocumented ritual
- considering “it launched somehow” equivalent to healthy startup
- skipping early observation of runtime condition

---

## 6. Final Rule

A serious platform must be started intentionally, not accidentally.

---

## 7. Status

This document is the active canonical startup runbook until replaced by a stricter startup operations reference.
