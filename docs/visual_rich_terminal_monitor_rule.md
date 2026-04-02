# VISUAL RICH TERMINAL MONITOR RULE v1

Status: active temporary monitor rule
Scope: read-only terminal visualization layer using Rich
Rule: Rich monitor may visualize canonical read models and runtime state, but may not own truth, mutate runtime, or bypass policy

---

## 1. Purpose

This document defines the rule for the temporary Rich-based terminal monitor.

It exists to allow:
- human-readable visual contact with the platform
- temporary operator visibility before full dashboard realization
- better comprehension of runtime state, tests, and canonical signals

without allowing:
- truth ownership drift
- runtime mutation through monitor UI
- hidden control-plane shortcuts

---

## 2. What the Rich Monitor Is

The Rich monitor is:

- temporary
- read-only
- operator-facing
- terminal-based
- presentation-only
- downstream from canonical truth sources

The Rich monitor is not:

- source of truth
- control-plane authority
- execution authority
- policy engine
- approval bypass path

---

## 3. Allowed Data Sources

The Rich monitor may read from canonical sources such as:

- RUNTIME/state/*.json
- logs/*.log
- canonical read models
- diagnostics snapshots
- test runtime summaries
- worker/process observations
- documented canonical status artifacts

---

## 4. Forbidden Behavior

The following remain forbidden:

- writing into CORE_ROOT
- mutating runtime state
- sending actions directly to workers
- acting as approval UI
- inventing synthetic truth
- showing decorative status that is not source-backed

---

## 5. Required Properties

The Rich monitor should remain:

- read-only
- traceable
- honest
- lightweight
- optional
- replaceable by future dashboard layers

---

## 6. Final Rule

The Rich monitor may improve visibility,
but it may not become a second control plane or a second truth layer.

---

## 7. Status

This document is the active rule for the temporary Rich terminal monitor until replaced by a stricter operator-monitor realization standard.
