# JARVIS-LIVE No-Drift Rules v0

Status: anti-drift policy document.

## Forbidden Parallel Worlds

JARVIS-LIVE must not create:

- a new AI registry
- a new worker registry
- a new agent world
- a new voice root
- a new memory engine
- a new runtime queue world
- a dashboard direct-execution path
- a raw shell path from an LLM
- a direct core-write path
- a hidden remote-control path
- a direct PC, phone, or app control path without allowlist and approval

## Required Reuse Surfaces

JARVIS-LIVE must reuse:

- `AI_SERVICES`
- `MAKSIMAR_CORE_LIB/ai_services`
- `MAKSIMAR_CORE_LIB/ai_orchestration`
- `MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding`
- `MAKSIMAR_CORE_LIB/workers_registry`
- `MAKSIMAR_CORE_LIB/workers_runtime`
- `MAKSIMAR_CORE_LIB/execution_control`
- `MAKSIMAR_CORE_LIB/memory_engine`
- `MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing`
- `MAKSIMAR_CORE_LIB/voice_layer`
- `MAKSIMAR_CORE_LIB/real_voice_runtime`
- `MAKSIMAR_SERVER/VOICE_ROUTING`
- `MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF`
- `MAKSIMAR_SERVER/VOICE_EXECUTION_HANDOFF`
- `MAKSIMAR_CORE_LIB/security_layer`
- `MAKSIMAR_CORE_LIB/oob_dashboard`

## Runtime Asset Rule

Model weights, vector indexes, embeddings, retrieval caches, and generated
runtime artifacts are runtime assets. They are not project truth and must not be
stored as canonical knowledge in the repository.

Project knowledge remains in:

- `MAKSIMAR_CORE_LIB/memory_engine`
- `runtime_history_store`
- app/chat memory domains
- retrieval indexes and references owned by memory/retrieval layers

## Dashboard Rule

Dashboard surfaces may show status, readiness, rejection reasons, queues,
latency, resource pressure, approval state, and audit evidence.

Dashboard surfaces must not start runtime, execute commands, mutate files,
control apps, control devices, download models, or bypass approval.

## Live Enablement Rule

JARVIS-LIVE can be considered for live runtime only after:

- voice gate is ready
- owner identity gate is ready
- action allowlist is ready
- approval binding is ready
- audit binding is ready
- dashboard status is ready
- model storage boundary is ready
- runtime vendor boundary is ready

Even then, live runtime must stay opt-in and disabled by default.
