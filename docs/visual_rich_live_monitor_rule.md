# VISUAL RICH LIVE MONITOR RULE v1

Status: active temporary live monitor rule
Scope: single-window Rich live terminal HUD for operator visibility
Rule: the live monitor may aggregate canonical read-only signals into one visual terminal window, but may not own truth, execute actions, or bypass policy

---

## 1. Purpose

This document defines the rule for the live Rich terminal monitor.

It exists to provide:
- one-window operator visibility
- structured visual contact with the platform
- temporary HUD-like monitoring before full dashboard realization

without allowing:
- runtime mutation
- hidden command execution
- truth ownership drift
- second control plane behavior

---

## 2. What the Live Monitor Is

The live monitor is:

- read-only
- terminal-based
- single-window
- operator-facing
- downstream from canonical truth sources
- temporary until full dashboard realization

The live monitor is not:

- execution UI
- approval UI
- write path
- source of truth
- control plane

---

## 3. Allowed Blocks

The live monitor may display blocks such as:

- header and system status
- platform tree
- governance/document summary
- worker/test summary
- logs and alerts
- read-only operator input or draft area

---

## 4. Forbidden Behavior

The following remain forbidden:

- direct runtime mutation
- action dispatch from monitor
- code execution from input area
- synthetic truth
- fake status decoration without source backing

---

## 5. Final Rule

The live monitor may improve situational awareness,
but it must remain a read-only presentation layer.

---

## 6. Status

This document is the active rule for the Rich live monitor until replaced by a stricter operator-monitor realization standard.
