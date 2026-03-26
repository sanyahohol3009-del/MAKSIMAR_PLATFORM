# DASHBOARD TRUTH CONTRACT v1

## Section 1 — Role
Current dashboard layer is a read-only observability shell.

It may:
- read state truth
- read diagnostic truth
- read API truth
- read session/process truth
- display current status
- display historical incidents as historical

It may not:
- mutate CORE_ROOT
- mutate runtime state as a control mechanism
- start services
- stop services
- bypass tools/work or tools/rest
- redefine source of truth

## Section 2 — Canonical truth inputs
Canonical dashboard truth inputs:
- RUNTIME/state/*.json
- logs/*.log
- /health
- /health/latency
- tmux session state
- process truth via pid/pgrep checks
- degraded/incident markers

## Section 3 — State semantics
Dashboard must distinguish:
- WARMING_UP
- ALIVE
- DEGRADED
- DEAD
- BROKEN
- HISTORICAL_INCIDENT

Required meaning:
- WARMING_UP = expected startup, truth not fully ready yet
- ALIVE = truth sources fresh and consistent
- DEGRADED = system alive but degraded flag/incident state active
- DEAD = runtime/process/session/API truth indicates service not alive
- BROKEN = truth mismatch or corrupted/contradictory state
- HISTORICAL_INCIDENT = past incident data, not current live failure

## Section 4 — Stale handling
Dashboard must never mix:
- current live state
- stale markers
- historical incidents

If marker is stale, dashboard must show it as stale/historical, not current failure.

## Section 5 — Panel classes
Operational truth panels:
- system status
- runtime / guard / kernel status
- logs / incidents / diagnostics

Node telemetry panels:
- CPU
- memory
- network

Engineering reference panels:
- project tree
- structural overview
- non-operational helper panels

## Section 6 — Alignment rule
Dashboard state presentation must align with truth-check logic.
Dashboard must not invent a weaker or alternate interpretation of liveness.

## Section 7 — Forbidden drift
Forbidden:
- dashboard action execution
- lifecycle logic inside dashboard
- truth definition inside wrapper scripts
- stale degraded markers shown as current state
- historical incidents shown as current live state
