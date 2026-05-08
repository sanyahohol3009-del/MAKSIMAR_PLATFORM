from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.ai_router_binding import (
    build_ai_router_memory_skill_binding_contract,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_skill_metrics_models import (
    MemorySkillMetricEntry,
    MemorySkillMetricsContract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)


def _is_multilingual_ready(
    *,
    supported_languages: tuple[str, ...],
    supported_scripts: tuple[str, ...],
) -> bool:
    """Check multilingual readiness for canonical project requirements."""
    required_languages = {"en", "ru", "uk", "de"}
    required_scripts = {"Latin", "Cyrillic"}
    return required_languages.issubset(set(supported_languages)) and required_scripts.issubset(
        set(supported_scripts)
    )


def build_memory_skill_metrics_contract() -> MemorySkillMetricsContract:
    """Build observability binding contract for memory and skills.

    This builder supports an extensible number of memory tiers, skills and
    router bindings. It must not assume a single canonical memory or skill entry.
    """
    memory_registry = build_memory_registry_contract()
    skill_registry = build_skill_adapter_registry_contract()
    ai_router_binding = build_ai_router_memory_skill_binding_contract()

    entries = []

    for memory_entry in memory_registry.entries:
        memory_multilingual_ready = _is_multilingual_ready(
            supported_languages=memory_entry.supported_languages,
            supported_scripts=memory_entry.supported_scripts,
        )
        entries.append(
            MemorySkillMetricEntry(
                metric_id=f"msmetric_memory_registry_{memory_entry.module_slug}",
                source_component="memory_registry",
                module_slug=memory_entry.module_slug,
                linked_memory_tier_id=memory_entry.memory_tier_id,
                linked_skill_id="",
                linked_worker_id="",
                linked_panel_id=memory_entry.panel_ids[0],
                route_request_id="",
                active=memory_entry.active,
                explanation_available=memory_entry.explanation_available,
                policy_compatible=True,
                multilingual_ready=memory_multilingual_ready,
                event_severity="info",
                alert_emitted=False,
                description=(
                    f"Observability metric for memory registry entry "
                    f"{memory_entry.module_slug}."
                ),
            )
        )

    for skill_entry in skill_registry.entries:
        skill_multilingual_ready = _is_multilingual_ready(
            supported_languages=skill_entry.supported_languages,
            supported_scripts=skill_entry.supported_scripts,
        )
        entries.append(
            MemorySkillMetricEntry(
                metric_id=f"msmetric_skill_registry_{skill_entry.module_slug}",
                source_component="skill_adapter_registry",
                module_slug=skill_entry.module_slug,
                linked_memory_tier_id="",
                linked_skill_id=skill_entry.skill_id,
                linked_worker_id=skill_entry.worker_id,
                linked_panel_id=skill_entry.panel_ids[0],
                route_request_id="",
                active=skill_entry.active,
                explanation_available=True,
                policy_compatible=True,
                multilingual_ready=skill_multilingual_ready,
                event_severity="info",
                alert_emitted=False,
                description=(
                    f"Observability metric for skill adapter registry entry "
                    f"{skill_entry.module_slug}."
                ),
            )
        )

    for route_entry in ai_router_binding.entries:
        entries.append(
            MemorySkillMetricEntry(
                metric_id=f"msmetric_{route_entry.route_request_id}",
                source_component="ai_router_binding",
                module_slug="simulation_analysis",
                linked_memory_tier_id=route_entry.selected_memory_tier_id,
                linked_skill_id=route_entry.selected_skill_id,
                linked_worker_id=route_entry.selected_worker_id,
                linked_panel_id=route_entry.selected_panel_id,
                route_request_id=route_entry.route_request_id,
                active=route_entry.active,
                explanation_available=route_entry.explanation_available,
                policy_compatible=route_entry.policy_compatible,
                multilingual_ready=route_entry.requested_language_code in ("en", "ru", "uk", "de")
                and route_entry.requested_script_name in ("Latin", "Cyrillic"),
                event_severity="info",
                alert_emitted=False,
                description=(
                    f"Observability metric for AI router binding {route_entry.route_request_id}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    explanation_ready_entries = sum(
        1 for entry in entries if entry.explanation_available
    )
    policy_compatible_entries = sum(
        1 for entry in entries if entry.policy_compatible
    )
    router_binding_entries = sum(
        1 for entry in entries if entry.source_component == "ai_router_binding"
    )

    return MemorySkillMetricsContract(
        total_entries=len(entries),
        active_entries=active_entries,
        explanation_ready_entries=explanation_ready_entries,
        policy_compatible_entries=policy_compatible_entries,
        router_binding_entries=router_binding_entries,
        entries=tuple(entries),
    )

