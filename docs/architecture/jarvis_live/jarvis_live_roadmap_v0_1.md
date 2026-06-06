# JARVIS-LIVE Roadmap v0.1

Status: roadmap/read-model only.

JARVIS-LIVE must remain disabled by default until the voice gate, owner identity gate,
action allowlist, approval binding, audit binding, dashboard status, model storage
boundary, and runtime vendor boundary are present and reviewed.

## Architecture Rule

JARVIS-LIVE extends existing platform surfaces:

- `AI_SERVICES`
- `MAKSIMAR_CORE_LIB/ai_orchestration`
- `MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding`
- `MAKSIMAR_CORE_LIB/workers_registry`
- `MAKSIMAR_CORE_LIB/workers_runtime`
- `MAKSIMAR_CORE_LIB/execution_control`
- `MAKSIMAR_CORE_LIB/memory_engine`
- `MAKSIMAR_CORE_LIB/voice_layer`
- `MAKSIMAR_CORE_LIB/real_voice_runtime`
- `MAKSIMAR_CORE_LIB/security_layer`
- `MAKSIMAR_CORE_LIB/oob_dashboard`

It must not create a parallel AI registry, worker registry, agent world, voice root,
memory engine, runtime queue, or dashboard execution path.

## Batches

### JL-0: Roadmap / CI / Anti-Drift Control

Files:

- `docs/architecture/jarvis_live/jarvis_live_roadmap_v0_1.md`
- `docs/architecture/jarvis_live/jarvis_live_no_drift_rules_v0.md`
- `MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_roadmap_status_builder.py`
- `tools/project_readiness_control/jarvis_live_roadmap_expected_files.py`
- `tests/jarvis_live/test_jarvis_live_roadmap_status_builder_smoke.py`
- `tests/jarvis_live/test_jarvis_live_no_parallel_world_guard_smoke.py`

Allowed scope: roadmap, read-model, anti-drift tests only.

### JL-1: Architecture / Contract Entry

Files already defined by Batch 1:

- `MAKSIMAR_CORE_LIB/ai_orchestration/jarvis_live_model_conductor_contract.py`
- `MAKSIMAR_CORE_LIB/real_voice_runtime/jarvis_live_disabled_gate_contract.py`
- `MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_readiness_summary_builder.py`
- `tests/jarvis_live/test_jarvis_live_contract_entry_smoke.py`

Allowed scope: contracts/read-models/tests only.

### JL-2: Model Profile / Resource Registry Binding

Purpose: bind model roles to existing AI services, router, workers, execution
control, and resource requirements. No model download.

### JL-3: Voice Disabled Status / Dashboard Binding

Purpose: expose microphone, wake-word, STT, TTS, and voice identity states as
read-only dashboard state. No audio runtime.

### JL-4: Screen Observer Vision Candidate Binding

Purpose: bind screen observer/OCR/vision candidates to existing read-only screen
observer and dashboard surfaces. No direct capture or app control.

### JL-5: Security / Approval / Action Allowlist Binding

Purpose: bind voice/action commands to owner identity, policy, approval, audit,
and action allowlist. No direct shell, core write, PC, phone, or app control.

### JL-6: External Task Broker Contract

Purpose: add Codex/Gemini-style task packet proposal contracts later. External
tools must be proposal producers, not direct executors.

### JL-7: Live Sandbox Vendor Boundary

Purpose: define storage/vendor/runtime boundaries for future live model assets.
Only after this boundary may models be downloaded outside git/core.

## Disabled Until

JARVIS-LIVE remains disabled until all of these are true:

- voice gate ready
- owner identity gate ready
- action allowlist ready
- approval binding ready
- audit binding ready
- dashboard status ready
- model storage boundary ready
- runtime vendor boundary ready

## Current Hard Blocks

- no runtime
- no model download
- no microphone
- no STT/TTS
- no wake word
- no app control
- no shell control
- no dashboard execution
- no direct core write
