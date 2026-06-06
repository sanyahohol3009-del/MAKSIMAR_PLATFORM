# JARVIS-LIVE Layer Context v0.1

JARVIS-LIVE is the operator-facing live assistant integration layer for the existing
MAKSIMAR platform. It is not a second AI platform, not a second agent world, and not
a runtime shortcut. Its job is to bind model roles, voice status, screen summaries,
security gates, queues, approvals, and dashboard read models into the architecture
that already exists.

JARVIS-LIVE extends these existing surfaces:

- AI_SERVICES
- ai_orchestration
- ai_router_binding
- workers_registry
- execution_control
- memory_engine
- runtime_history_store
- voice_layer
- real_voice_runtime
- VOICE_ROUTING, VOICE_DISPLAY_HANDOFF, and VOICE_EXECUTION_HANDOFF
- security_layer
- oob_dashboard

The integration rule is reuse-first. There must be no new AI registry, no new worker
registry, no new agent world, no new runtime queue, no new memory engine, and no new
voice root. New JARVIS-LIVE entries must be contracts, bindings, read models, or
tests that point into the existing surfaces.

Model weights are runtime assets, not project knowledge. They belong behind the
runtime storage and vendor boundaries, outside git/core truth, and only after the
download gate is ready. Project knowledge stays in memory_engine/history_ingestion,
runtime_history_store, app/chat memory, retrieval indexes, embeddings, vector
storage, and retrieval cache layers.

Current roadmap status:

- JL-0 Roadmap / CI / Anti-Drift Control is READY.
- JL-1 JARVIS-LIVE Contract Entry is READY.
- JL-2 Model Profile / Resource Registry Binding is NEXT.
- JL-10 blocks model downloads until storage and vendor boundaries are ready.
- JL-11 is the first voice smoke milestone; voice live remains blocked before it.
- JL-14 is the first controlled PC action adapter milestone; PC control remains
  blocked before it.

Security and network rules are strict. There is no hidden remote control, no raw
shell access from an LLM, and no direct PC, phone, file, app, or shell control
without an allowlist, approval binding, audit binding, and dashboard-visible status.
Dashboard surfaces stay read-only and are not a source of execution truth.

