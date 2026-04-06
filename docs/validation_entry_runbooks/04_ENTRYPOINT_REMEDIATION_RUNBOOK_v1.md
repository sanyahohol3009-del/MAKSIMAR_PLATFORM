# 04 ENTRYPOINT REMEDIATION RUNBOOK v1

Status: active canonical entrypoint-remediation runbook
Scope: operator recovery when validation is launched with a weak or ambiguous pytest entrypoint
Rule: entrypoint ambiguity must be corrected explicitly so validation results are interpreted under the intended launch mode

---

## 1. Purpose

This document defines the entrypoint-remediation runbook of the platform.

It exists to preserve:
- explicit correction of launch-mode ambiguity
- continuity between command policy and operator recovery
- reduced confusion after collection-stage red output
- a stable base for later wrapper enforcement

---

## 2. Remediation Principle

Entrypoint remediation should remain understandable in terms of:
- identifying ambiguous or weak launch mode
- selecting the trusted fallback or preferred command
- rerunning validation under canonical interpretation
- comparing results only after launch ambiguity is removed

---

## 3. Required Rule

Entrypoint remediation should remain:
- explicit
- command-aware
- bootstrap-aware
- fallback-aware
- diagnostics-aligned

---

## 4. What Is Forbidden

The following remain forbidden:
- persisting with ambiguous commands after they proved unreliable
- treating launch ambiguity as harmless
- forgetting the difference between fallback and fast path
- trusting weak launch behavior without interpretation

---

## 5. Final Rule

A mature validation workflow fixes the command path before it trusts the outcome.

---

## 6. Status

This document is the active canonical entrypoint-remediation runbook until replaced by a stricter validation launch recovery reference.
