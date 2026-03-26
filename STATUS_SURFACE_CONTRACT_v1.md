# STATUS SURFACE CONTRACT v1

## Section 1 — Role
Current status surfaces are the canonical read-only operator status views for the foundation layer.

They are:
- tools/ctl status
- tools/guard_ctl status
- tools/core_guard_ctl status
- tools/kernel_guard_ctl status

They must:
- reflect canonical operational truth
- expose session/process/heartbeat/api state consistently
- distinguish current state from stale/invalid/missing truth
- remain read-only

They must not:
- execute business logic
- redefine source of truth
- hide truth mismatches
- act as lifecycle orchestration
- bypass work/rest

## Section 2 — Canonical truth inputs
Status surfaces may read only:
- RUNTIME/state/*.json
- logs/*.log
- tmux session state
- pid/process truth
- /health
- /health/latency
- degraded markers

## Section 3 — Required state semantics
Canonical visible state values:
- WARMING_UP
- ALIVE
- DEGRADED
- DEAD
- BROKEN

Meaning:
- WARMING_UP = startup in progress, truth not fully established yet
- ALIVE = truth sources fresh and consistent
- DEGRADED = system alive but degraded marker active
- DEAD = required truth missing/stale and service not alive
- BROKEN = contradictory or invalid truth

## Section 4 — Required status blocks
Every status surface must expose:
- tmux
- process
- heartbeat
- state
- truth

Runtime status additionally exposes:
- port
- http
- degraded

## Section 5 — Consistency rules
- heartbeat output must use the same semantics across all status surfaces
- invalid heartbeat must not be shown as alive
- stale heartbeat must not be shown as warming_up forever
- missing tmux + present process or present tmux + missing process should be treated as truth mismatch candidates
- core_guard_ctl must not use weaker heartbeat formatting than guard_ctl or kernel_guard_ctl

## Section 6 — Dashboard shell dependency
tools/dashboard is only a tmux shell over status surfaces.
Therefore status surfaces are the real current observability panels and must be hardened before STEP 46.

## Section 7 — Forbidden drift
Forbidden:
- inconsistent ALIVE/NOT_ALIVE semantics between surfaces
- ad-hoc custom formatting in only one surface
- stale state shown as current health
- wrappers becoming logic layers
