from __future__ import annotations


JARVIS_LIVE_ROADMAP_EXPECTED_FILES: tuple[dict[str, str], ...] = (
    {
        "path": "docs/architecture/jarvis_live/jarvis_live_roadmap_v0_1.md",
        "role": "doc",
        "description": "JARVIS-LIVE roadmap v0.1.",
    },
    {
        "path": "docs/architecture/jarvis_live/jarvis_live_no_drift_rules_v0.md",
        "role": "doc",
        "description": "JARVIS-LIVE anti-drift rules.",
    },
    {
        "path": "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/jarvis_live_roadmap_status_builder.py",
        "role": "source",
        "description": "Read-only JARVIS-LIVE roadmap status builder.",
    },
    {
        "path": "tools/project_readiness_control/jarvis_live_roadmap_expected_files.py",
        "role": "tool",
        "description": "Expected files and no-parallel-world guard constants wrapper.",
    },
    {
        "path": "tests/jarvis_live/test_jarvis_live_roadmap_status_builder_smoke.py",
        "role": "test",
        "description": "Roadmap status builder smoke test.",
    },
    {
        "path": "tests/jarvis_live/test_jarvis_live_no_parallel_world_guard_smoke.py",
        "role": "test",
        "description": "No parallel world guard smoke test.",
    },
)


JARVIS_LIVE_REQUIRED_EXISTING_SURFACES: tuple[str, ...] = (
    "AI_SERVICES",
    "MAKSIMAR_CORE_LIB/ai_services",
    "MAKSIMAR_CORE_LIB/ai_orchestration",
    "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
    "MAKSIMAR_CORE_LIB/workers_registry",
    "MAKSIMAR_CORE_LIB/workers_runtime",
    "MAKSIMAR_CORE_LIB/execution_control",
    "MAKSIMAR_CORE_LIB/memory_engine",
    "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",
    "MAKSIMAR_CORE_LIB/voice_layer",
    "MAKSIMAR_CORE_LIB/real_voice_runtime",
    "MAKSIMAR_SERVER/VOICE_ROUTING",
    "MAKSIMAR_SERVER/VOICE_DISPLAY_HANDOFF",
    "MAKSIMAR_SERVER/VOICE_EXECUTION_HANDOFF",
    "MAKSIMAR_CORE_LIB/security_layer",
    "MAKSIMAR_CORE_LIB/oob_dashboard",
)


FORBIDDEN_PARALLEL_WORLD_ROOTS: tuple[str, ...] = (
    "JARVIS_LIVE_AI_REGISTRY",
    "JARVIS_LIVE_WORKER_REGISTRY",
    "JARVIS_LIVE_AGENT_WORLD",
    "JARVIS_LIVE_VOICE_ROOT",
    "JARVIS_LIVE_MEMORY_ENGINE",
    "JARVIS_LIVE_RUNTIME_QUEUE",
    "MAKSIMAR_CORE_LIB/jarvis_live_ai_registry",
    "MAKSIMAR_CORE_LIB/jarvis_live_worker_registry",
    "MAKSIMAR_CORE_LIB/jarvis_live_agents",
    "MAKSIMAR_CORE_LIB/jarvis_live_memory_engine",
    "MAKSIMAR_CORE_LIB/jarvis_live_runtime_queue",
    "MAKSIMAR_SERVER/JARVIS_LIVE_DIRECT_EXECUTION",
)


def list_jarvis_live_roadmap_expected_paths() -> tuple[str, ...]:
    return tuple(entry["path"] for entry in JARVIS_LIVE_ROADMAP_EXPECTED_FILES)
