# FOUNDATION INTEGRATION CONTRACT v1

## SECTION 1 — CORE
Canonical safety/runtime foundation:
- CORE_ROOT
- SUPERVISOR
- RUNTIME/state
- logs
- tools/work
- tools/rest
- tools/ctl
- tools/guard_ctl
- tools/core_guard_ctl
- tools/kernel_guard_ctl

Role:
- lifecycle
- safety chain
- heartbeat truth
- process truth
- shutdown/startup discipline

## SECTION 2 — OPERATOR LAYER
Canonical operator lifecycle layer:
- ./tools/work
- ./tools/rest
- ctl family

Strict role:
- start order
- stop order
- heartbeat validation
- truth checks
- stale state cleanup

Forbidden:
- business logic
- AI logic
- UI logic
- dashboard logic
- routing decisions
- policy execution

## SECTION 3 — CURRENT DASHBOARD SHELL
Current operator observability shell:
- tools/dashboard
- tools/dashboard.sh
- tools/dashboards_open

Role:
- read-only observability shell
- operator engineering visibility
- fallback monitoring surface

Not:
- source of truth
- main dashboard
- action executor
- lifecycle controller

## SECTION 4 — SOURCE OF TRUTH
Canonical truth interfaces:
- RUNTIME/state/*.json
- logs/*.log
- tmux session state
- /health
- /health/latency

Rules:
- dashboard reads truth
- dashboard never defines truth
- operator shell never mutates truth
- main dashboard must read the same truth interfaces

## SECTION 5 — LIFECYCLE RULES
Canonical start:
- ./tools/work

Canonical stop:
- ./tools/rest

Strict startup order:
- runtime
- guard
- core guard
- kernel watchdog

Strict shutdown order:
- kernel watchdog
- core guard
- guard
- runtime

Forbidden:
- manual direct start of individual runtime components
- bypass of work/rest

## SECTION 6 — LEGACY VS CANONICAL DASHBOARD RULE
Legacy operator dashboards:
- remain alive
- remain read-only
- act as fallback/operator surfaces

Future canonical dashboard:
- becomes unified operator UI
- must not replace truth interfaces
- must not duplicate lifecycle control
- may embed derived summaries from legacy observability shell

## SECTION 7 — FORBIDDEN DRIFT
Forbidden:
- new dashboard root
- new display manager root
- new gesture root
- new navigation root
- action logic inside source_of_truth
- action logic inside runtime_observability
- action logic inside physics_dashboard_views
- action logic inside display topology contracts
- direct gesture/voice bypass of placement/control-plane

## SECTION 8 — NEXT INTEGRATION STEP
Before STEP 46:
1. classify current operational/dashboard files
2. classify truth interfaces
3. classify legacy-risk files
4. keep lifecycle path canonical
5. keep dashboards read-only
6. prepare legacy dashboard registry mapping
