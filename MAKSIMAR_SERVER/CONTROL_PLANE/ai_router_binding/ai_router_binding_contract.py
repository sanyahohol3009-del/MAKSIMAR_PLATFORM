from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_memory_classification_policy_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.ai_router_binding.ai_router_binding_models import (
    AiRouterMemorySkillBindingContract,
    AiRouterMemorySkillBindingEntry,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)


def build_ai_router_memory_skill_binding_contract() -> AiRouterMemorySkillBindingContract:
    """Build canonical AI router memory/skill binding contract."""
    memory_policy = build_memory_classification_policy_contract()
    memory_registry = build_memory_registry_contract()
    skill_registry = build_skill_adapter_registry_contract()

    if len(memory_policy.entries) != 1:
        raise ValueError("Expected exactly one canonical memory policy entry")

    if len(memory_registry.entries) != 1:
        raise ValueError("Expected exactly one canonical memory registry entry")

    if len(skill_registry.entries) != 1:
        raise ValueError("Expected exactly one canonical skill registry entry")

    memory_policy_entry = memory_policy.entries[0]
    memory_registry_entry = memory_registry.entries[0]
    skill_registry_entry = skill_registry.entries[0]

    if memory_policy_entry.memory_tier_id != memory_registry_entry.memory_tier_id:
        raise ValueError("Memory policy and memory registry tier ids must match")

    if not skill_registry_entry.active:
        raise ValueError("Skill registry entry must be active")

    if not memory_registry_entry.active:
        raise ValueError("Memory registry entry must be active")

    accepted_fact_classes = memory_policy_entry.accepted_fact_classes

    required_fact_classes = (
        "architecture_decision",
        "platform_invariant",
        "roadmap_checkpoint",
    )
    for fact_class in required_fact_classes:
        if fact_class not in accepted_fact_classes:
            raise ValueError(f"Missing accepted fact class: {fact_class}")

    entries = (
        AiRouterMemorySkillBindingEntry(
            route_request_id="route_architecture_decision_001",
            requested_fact_class="architecture_decision",
            requested_language_code="ru",
            requested_script_name="Cyrillic",
            selected_skill_id=skill_registry_entry.skill_id,
            selected_worker_id=skill_registry_entry.worker_id,
            selected_memory_tier_id=memory_registry_entry.memory_tier_id,
            retrieval_scope_id="memscope_architecture_decision_001",
            selected_panel_id=skill_registry_entry.panel_ids[0],
            route_mode="skill_plus_memory",
            route_status="bound",
            policy_compatible=True,
            explanation_available=memory_registry_entry.explanation_available,
            active=skill_registry_entry.active and memory_registry_entry.active,
            description=(
                "AI router binding for architecture decision retrieval using the "
                "simulation analysis skill and foundational memory tier."
            ),
        ),
        AiRouterMemorySkillBindingEntry(
            route_request_id="route_platform_invariant_001",
            requested_fact_class="platform_invariant",
            requested_language_code="de",
            requested_script_name="Latin",
            selected_skill_id=skill_registry_entry.skill_id,
            selected_worker_id=skill_registry_entry.worker_id,
            selected_memory_tier_id=memory_registry_entry.memory_tier_id,
            retrieval_scope_id="memscope_platform_invariant_001",
            selected_panel_id=skill_registry_entry.panel_ids[0],
            route_mode="skill_plus_memory",
            route_status="bound",
            policy_compatible=True,
            explanation_available=memory_registry_entry.explanation_available,
            active=skill_registry_entry.active and memory_registry_entry.active,
            description=(
                "AI router binding for platform invariant retrieval using the "
                "simulation analysis skill and foundational memory tier."
            ),
        ),
        AiRouterMemorySkillBindingEntry(
            route_request_id="route_roadmap_checkpoint_001",
            requested_fact_class="roadmap_checkpoint",
            requested_language_code="en",
            requested_script_name="Latin",
            selected_skill_id=skill_registry_entry.skill_id,
            selected_worker_id=skill_registry_entry.worker_id,
            selected_memory_tier_id=memory_registry_entry.memory_tier_id,
            retrieval_scope_id="memscope_roadmap_checkpoint_001",
            selected_panel_id=skill_registry_entry.panel_ids[0],
            route_mode="skill_plus_memory",
            route_status="bound",
            policy_compatible=True,
            explanation_available=memory_registry_entry.explanation_available,
            active=skill_registry_entry.active and memory_registry_entry.active,
            description=(
                "AI router binding for roadmap checkpoint retrieval using the "
                "simulation analysis skill and foundational memory tier."
            ),
        ),
    )

    active_entries = sum(1 for entry in entries if entry.active)
    explanation_ready_entries = sum(
        1 for entry in entries if entry.explanation_available
    )
    policy_compatible_entries = sum(
        1 for entry in entries if entry.policy_compatible
    )

    return AiRouterMemorySkillBindingContract(
        total_entries=len(entries),
        active_entries=active_entries,
        explanation_ready_entries=explanation_ready_entries,
        policy_compatible_entries=policy_compatible_entries,
        entries=entries,
    )
