# FOUNDATION STARTUP CONTRACT v1

## Section 1 — Purpose
Foundation startup and shutdown must be canonical, staged, and safe.

The system must not require ad-hoc manual command sequences.
Operator UI buttons may exist later, but they must call canonical lifecycle entrypoints.

## Section 2 — Canonical lifecycle entrypoints
Canonical startup:
- ./tools/work

Canonical shutdown:
- ./tools/rest

Forbidden:
- starting runtime manually outside canonical path
- starting guard/core/kernel in arbitrary order
- bypassing lifecycle scripts from UI/operator layer

## Section 3 — Startup order
Canonical startup order:

1. stale state cleanup
2. runtime start
3. runtime heartbeat ready
4. guard start
5. guard heartbeat ready
6. core guard start
7. core guard heartbeat ready
8. kernel watchdog start
9. kernel heartbeat ready
10. dashboard shell open (best effort only)

Formal order:
- runtime
- stop-gate watcher
- core guard
- kernel watchdog

## Section 4 — Shutdown order
Canonical shutdown order:

1. kernel watchdog stop
2. core guard stop
3. stop-gate watcher stop
4. runtime stop
5. stale state cleanup

Shutdown must be reverse to startup safety order.

## Section 5 — Readiness semantics
Foundation stages must be interpreted as:

- NOT_STARTED
- WARMING_UP
- READY
- DEGRADED
- BROKEN
- STOPPED

Meaning:
- NOT_STARTED = stage not launched
- WARMING_UP = stage launched but truth not yet established
- READY = stage truth established
- DEGRADED = stage/system alive but degraded marker active
- BROKEN = contradictory truth or failed startup path
- STOPPED = stage fully stopped

## Section 6 — Stage readiness requirements
Runtime READY requires:
- tmux session present
- process present
- heartbeat fresh
- port listening
- /health available

Guard READY requires:
- tmux session present
- process present
- heartbeat fresh

Core guard READY requires:
- tmux session present
- process present
- heartbeat fresh

Kernel watchdog READY requires:
- tmux session present
- process present
- heartbeat fresh

## Section 7 — Dashboard relation
Current dashboard shell is not a startup authority.
It may only display lifecycle state.

tools/dashboard:
- may open status windows
- may attach to sessions
- may display truth

tools/dashboard may not:
- redefine readiness
- start foundation directly
- stop foundation directly
- bypass work/rest

## Section 8 — Future operator UI relation
Future Start button:
- must invoke canonical startup path
- must not implement its own startup order

Future Stop button:
- must require confirmation
- must invoke canonical shutdown path

Future Sleep button:
- must be a separate controlled lifecycle mode
- must not be treated as raw stop/kill
- requires separate contract later

## Section 9 — Cleanup rules
Canonical startup must clean stale transient state before stage launch.
Canonical shutdown must clean stale transient state after stop.

Cleanup may include:
- heartbeat state files
- transient pid files
- stale degraded markers when appropriate

Cleanup must not:
- destroy canonical logs
- destroy historical incident evidence
- mutate immutable core artifacts

## Section 10 — Forbidden drift
Forbidden:
- multiple independent startup paths
- direct UI lifecycle logic
- dashboard becoming lifecycle controller
- manual out-of-order guard startup
- mixing startup hardening with STEP 46+
- treating optional surfaces as readiness truth

## Section 11 — Target operational model
Target user experience:

- open system
- press Start
- system performs canonical staged startup
- system becomes observable
- system becomes operator-usable

- press Stop
- confirmation dialog shown
- canonical staged shutdown executes
- transient runtime clutter cleaned safely

This user experience must be implemented later through operator UI,
but foundation lifecycle semantics must be finalized first.
