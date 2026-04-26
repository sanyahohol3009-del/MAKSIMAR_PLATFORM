# JARVIS PHASE 12 — FRONTEND SHELL / REGISTRY / BINDING CANONICAL

## Status
This document fixes the canonical state of PHASE 12 for JARVIS.

Current confirmed status:
- PHASE 12.1 — Shell Foundation: closed
- PHASE 12.2 — Registry / State: closed
- PHASE 12.3 — Chat / Explain / Command Split: closed

PHASE 12 is canonical-ready.

---

## Purpose of PHASE 12
PHASE 12 defines the frontend shell, registry/state layer, and interaction split layer.

This phase exists so that JARVIS does not expose a random frontend or uncontrolled application shell.
Instead, the visible frontend must be:
- shell-structured
- registry-driven
- state-bound
- interaction-split
- truth-bound

PHASE 12 is not a giant app shell.
PHASE 12 is not a direct execution layer.
PHASE 12 is the canonical frontend shell / registry / binding layer.

---

## Canonical PHASE 12 order

Correct order for this phase:

1. Shell Foundation
2. Registry / State
3. Chat / Explain / Command Split

Meaning:
first the shell structure,
then registry/state bindings,
then separation of chat, explainability, and command paths.

---

## PHASE 12.1 — Shell Foundation

### Purpose
This step formalizes the canonical frontend shell structure.

### Canonical contracts
- dashboard_shell_contract.ts
- sidebar_contract.ts
- top_status_bar_contract.ts
- workspace_frame_contract.ts
- explain_panel_contract.ts
- command_strip_contract.ts

### Canonical meaning
Shell foundation must guarantee:
- a canonical dashboard shell exists
- sidebar exists
- top status bar exists
- workspace frame exists
- explain panel exists
- command strip exists

### Hard rules
- no giant app shell
- no uncontrolled shell growth
- no direct server mutation through command strip
- explain panel remains read-only explainability bound

---

## PHASE 12.2 — Registry / State

### Purpose
This step formalizes registry-driven shell behavior and active state management.

### Canonical contracts
- panel_registry_contract.ts
- shell_state_contract.ts
- view_binding_contract.ts
- workspace_switch_contract.ts

### Canonical meaning
Registry/state layer must guarantee:
- panels are registry-bound
- active shell state is explicit
- views are bound to zones
- workspace switching is explicit and guarded

### Hard rules
- registry state correctness
- active view validity
- no hidden panel routing
- no uncontrolled workspace switching

---

## PHASE 12.3 — Chat / Explain / Command Split

### Purpose
This step formalizes the separation between chat, explainability, and command handling.

### Canonical contracts
- chat_panel_contract.ts
- explain_view_contract.ts
- command_queue_view_contract.ts
- interaction_split_contract.ts

### Canonical meaning
This layer must guarantee:
- chat is its own path
- explainability is its own read-only path
- command queue is its own guarded path
- split semantics are explicit

### Hard rules
- separation of concerns
- no command -> direct server action
- explainability stays read-only
- command path stays guarded

---

## PHASE 12 canonical semantics

PHASE 12 means:

shell foundation
-> registry/state
-> chat/explain/command split

This is the canonical frontend assembly path for JARVIS.

Meaning:
frontend is no longer an accidental UI fragment;
it is a contract-bound operator shell with explicit bindings and explicit interaction separation.

---

## What PHASE 12 does not allow

PHASE 12 must never:
- create one giant uncontrolled frontend shell
- bypass registry/state contracts
- mix chat and command into one uncontrolled path
- allow explainability to mutate runtime
- allow command path to directly mutate server state
- bypass guarded interaction semantics

---

## Acceptance meaning of PHASE 12
After PHASE 12, the platform guarantees:

- a canonical shell foundation exists
- panel registry and shell state exist
- workspace and view bindings exist
- chat, explain, and command are separated
- the frontend shell is operator-ready

Therefore:
the frontend is now a governed shell layer rather than an improvised UI layer.

---

## Canonical completion statement
PHASE 12 is closed only when:
- all shell foundation contracts exist
- all registry/state contracts exist
- all chat/explain/command split contracts exist
- TypeScript compilation is clean
- tests are green
- previews are working
- no direct command -> server mutation path exists

PHASE 12 is now fixed as the canonical frontend shell / registry / binding layer for JARVIS.
