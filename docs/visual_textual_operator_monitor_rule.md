# VISUAL TEXTUAL OPERATOR MONITOR RULE v1

Status: active temporary textual monitor rule
Scope: single-window terminal UI with live panels and editable draft area
Rule: the Textual operator monitor may provide editable draft input in one window, but may not own truth, execute actions, or bypass policy

---

## 1. Purpose

This document defines the rule for the temporary Textual-based operator monitor.

It exists to allow:
- one-window terminal UI
- live operator visibility
- editable draft/code pane
- temporary visual contact before full dashboard realization

without allowing:
- runtime mutation
- code execution from monitor
- truth ownership drift
- hidden control-plane shortcuts

---

## 2. What the Textual Monitor Is

The Textual monitor is:

- temporary
- read-only with respect to platform truth
- editable only in its local draft area
- operator-facing
- terminal-based
- downstream from canonical truth sources

The Textual monitor is not:

- source of truth
- execution authority
- approval UI
- control plane
- runtime mutation path

---

## 3. Allowed Blocks

The Textual monitor may display:

- header and status
- system overview
- governance/documents summary
- platform tree
- worker pulse
- live logs
- editable draft/code pane

---

## 4. Forbidden Behavior

The following remain forbidden:

- direct runtime mutation
- action dispatch into workers
- code execution from the editor pane
- synthetic truth
- fake status decoration without source backing

---

## 5. Final Rule

The Textual monitor may improve operator visibility and comfort,
but it must remain a read-only monitor with a local editable draft area only.

---

## 6. Status

This document is the active rule for the temporary Textual operator monitor until replaced by a stricter operator-dashboard realization standard.
