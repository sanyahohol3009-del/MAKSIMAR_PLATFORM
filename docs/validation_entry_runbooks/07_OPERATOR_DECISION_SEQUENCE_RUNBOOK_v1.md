# 07 OPERATOR DECISION SEQUENCE RUNBOOK v1

Status: active canonical operator-decision-sequence runbook
Scope: ordered human decision path for validation entry trouble
Rule: the operator should have a readable decision sequence so recovery remains bounded and repeatable

---

## 1. Purpose

This document defines the operator-decision-sequence runbook of the platform.

It exists to preserve:
- ordered operator reasoning
- lower restart cost during diagnostics
- bounded remediation sequence
- a stable base for later runbook families and helper tooling

---

## 2. Decision Principle

Operator decision sequence should remain understandable in terms of:
- what to check first
- what to check second
- when to retry
- when to switch to fallback
- when validation meaning is strong enough to trust again

---

## 3. Canonical Sequence

The operator should conceptually follow this order:

1. confirm correct project root
2. confirm correct virtual environment and tool resolution
3. confirm correct validation entrypoint
4. decide whether fast or fallback execution is appropriate
5. interpret whether failure is entry-stage, collection-stage, or executed-test-stage
6. rerun only after the earlier ambiguity is resolved

---

## 4. What Is Forbidden

The following remain forbidden:
- random troubleshooting order
- skipping foundational checks
- escalating to deeper debugging too early
- trusting reruns that preserved the same broken launch conditions

---

## 5. Final Rule

A mature platform gives the operator an ordered path, not just a pile of possible checks.

---

## 6. Status

This document is the active canonical operator-decision-sequence runbook until replaced by a stricter operator recovery reference.
