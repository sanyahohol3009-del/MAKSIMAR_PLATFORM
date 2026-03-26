from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)
from MAKSIMAR_SERVER.INTENT_NORMALIZATION import (
    build_intent_normalization_contract,
)
from MAKSIMAR_SERVER.VOICE_ROUTING.voice_routing_models import (
    VoiceRoutingContract,
    VoiceRoutingEntry,
)


def build_voice_routing_contract() -> VoiceRoutingContract:
    """Build canonical voice routing / intent binding contract."""
    intent_normalization = build_intent_normalization_contract()
    display_orchestration = build_display_orchestration_contract()
    explainable_binding = build_explainable_view_binding_contract()

    display_route_by_id = {
        entry.route_request_id: entry for entry in display_orchestration.entries
    }
    explainable_by_view_id = {
        entry.view_id: entry for entry in explainable_binding.entries
    }

    entries = []
    for intent_entry in intent_normalization.entries:
        if intent_entry.intent_source != "voice":
            continue

        display_entry = display_route_by_id[
            _resolve_display_route_id(intent_entry.intent_id)
        ]
        explainable_entry = explainable_by_view_id[intent_entry.target_view_id]

        entries.append(
            VoiceRoutingEntry(
                voice_route_id=_resolve_voice_route_id(intent_entry.intent_id),
                intent_id=intent_entry.intent_id,
                intent_source=intent_entry.intent_source,
                source_command_id=intent_entry.source_command_id,
                command_intent=_resolve_command_intent(intent_entry.intent_id),
                target_display_route_id=display_entry.route_request_id,
                target_view_id=intent_entry.target_view_id,
                target_display_role=intent_entry.target_display_role,
                target_panel_id=display_entry.selected_panel_id,
                routing_mode="normalized_intent_to_display_route",
                low_latency_required=intent_entry.low_latency_required,
                explanation_required=(
                    intent_entry.explanation_required
                    and explainable_entry.explanation_text_available
                ),
                multilingual_ready=(
                    intent_entry.multilingual_ready
                    and explainable_entry.multilingual_ready
                    and display_entry.multilingual_ready
                ),
                active=intent_entry.active,
                route_status="bound",
                description=(
                    f"Voice routing binding for normalized intent {intent_entry.intent_id} "
                    f"toward {intent_entry.target_display_role}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    low_latency_entries = sum(
        1 for entry in entries if entry.low_latency_required
    )
    explanation_required_entries = sum(
        1 for entry in entries if entry.explanation_required
    )
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )

    return VoiceRoutingContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        explanation_required_entries=explanation_required_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )


def _resolve_voice_route_id(intent_id: str) -> str:
    """Resolve canonical voice route id from normalized intent id."""
    if intent_id == "intent_show_memory_001":
        return "voiceroute_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "voiceroute_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "voiceroute_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_display_route_id(intent_id: str) -> str:
    """Resolve canonical display route id from normalized intent id."""
    if intent_id == "intent_show_memory_001":
        return "displayroute_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "displayroute_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "displayroute_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_command_intent(intent_id: str) -> str:
    """Resolve command intent from normalized intent id."""
    if intent_id == "intent_show_memory_001":
        return "show_memory"
    if intent_id == "intent_show_simulation_001":
        return "show_simulation"
    if intent_id == "intent_show_monitoring_001":
        return "show_monitoring"
    raise ValueError(f"Unsupported intent_id: {intent_id}")
