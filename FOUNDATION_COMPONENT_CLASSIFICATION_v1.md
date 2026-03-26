# FOUNDATION COMPONENT CLASSIFICATION v1

## Canonical operational layer
- CORE_ROOT/runtime_paths.py
- CORE_ROOT/run_context.py
- CORE_ROOT/core_guard.py
- CORE_ROOT/stop_gate.py
- CORE_ROOT/stop_gate_watcher.py
- CORE_ROOT/kernel_watchdog.py
- CORE_ROOT/core_integrity_verifier.py
- CORE_ROOT/heartbeat_io.py
- SUPERVISOR/process_supervisor.py
- tools/work
- tools/rest
- tools/ctl
- tools/guard_ctl
- tools/core_guard_ctl
- tools/kernel_guard_ctl

Status note:
- these files form the current canonical safety/runtime/operator foundation
- lifecycle control must continue to flow only through tools/work and tools/rest
- no business logic, UI logic, AI logic, routing logic, or policy execution may be added here

## Canonical truth interfaces
- RUNTIME/state/*.json
- logs/*.log
- tmux session state
- /health
- /health/latency

Status note:
- these interfaces are the current source of operational truth
- dashboards and future operator surfaces must read truth from these interfaces only
- truth must not be redefined inside dashboard shells or wrapper scripts

## Canonical current dashboard shell
- tools/dashboard

Status note:
- tools/dashboard is the current canonical operator observability shell entrypoint
- it is read-only
- it is not the main dashboard
- it is not a source-of-truth layer
- it is not an action executor
- it is not a lifecycle controller

## Support-only wrappers
- tools/dashboard.sh
- tools/dashboards_open

Status note:
- these wrappers are support-only entrypoints around tools/dashboard
- they must not evolve into separate dashboard logic layers
- they must not become orchestration or truth-definition surfaces

## Legacy-risk / duplicate candidates
- CORE_ROOT/rantime_paths.py
- CORE_ROOT/ru_context.py

Status note:
- no active imports found in repository code
- references observed only in .mypy_cache
- canonical files are:
  - CORE_ROOT/runtime_paths.py
  - CORE_ROOT/run_context.py
- cleanup should be done in a dedicated small pass, not mixed into STEP 46

## Ambiguous / needs later classification
- SUPERVISOR/watchdog.py
- RUNTIME/runtime_guard.py
- RUNTIME/recovery_manager.py

Status note:
- these files are not currently classified as canonical operational layer
- they are not currently approved as removal targets
- they require a later dedicated audit before any cleanup, migration, or reuse decision

## Classification rules
- canonical = active, approved, architecturally current
- support-only = allowed helper/wrapper, but not a source-of-truth or main logic layer
- legacy-risk = likely duplicate, typo, drift, or obsolete candidate; do not extend further
- ambiguous = requires dedicated audit before classification change

## Forbidden drift
- do not create new dashboard roots
- do not create new display manager roots
- do not create new gesture roots
- do not move lifecycle logic into dashboards
- do not move truth definition into wrappers
- do not add action execution into current dashboard shell
- do not mix cleanup of legacy-risk files into STEP 46 or later dashboard/display work

## Immediate next rule
- finish foundation integration documentation
- isolate legacy-risk files in a dedicated cleanup mini-pass
- only after clean foundation classification proceed to STEP 46
