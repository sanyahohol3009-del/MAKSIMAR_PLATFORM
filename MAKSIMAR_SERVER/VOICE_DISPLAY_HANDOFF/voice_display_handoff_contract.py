from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)
from MAKSIMAR_SERVER.VOICE_DISPLAY_HANDOFF.voice_display_handoff_models import (
    VoiceDisplayHandoffContract,
    VoiceDisplayHandoffEntry,
)
from MAKSIMAR_SERVER.VOICE_ROUTING import (
    build_voice_routing_contract,
)


def build_voice_display_handoff_contract() -> VoiceDisplayHandoffContract:
    """Build canonical voice display / explanation handoff contract."""
    voice_routing = build_voice_routing_contract()
    display_orchestration = build_display_orchestration_contract()
    explainable_binding = build_explainable_view_binding_contract()

    display_route_by_id = {
        entry.route_request_id: entry for entry in display_orchestration.entries
    }
    explainable_by_view_id = {
        entry.view_id: entry for entry in explainable_binding.entries
    }

    entries = []
    for voice_entry in voice_routing.entries:
        display_entry = display_route_by_id[voice_entry.target_display_route_id]
        explainable_entry = explainable_by_view_id[voice_entry.target_view_id]

        if display_entry.selected_panel_id != voice_entry.target_panel_id:
            raise ValueError(
                f"Display orchestration panel mismatch for {voice_entry.voice_route_id}"
            )

        if display_entry.selected_display_role != voice_entry.target_display_role:
            raise ValueError(
                f"Display orchestration role mismatch for {voice_entry.voice_route_id}"
            )

        entries.append(
            VoiceDisplayHandoffEntry(
                handoff_id=_resolve_handoff_id(voice_entry.intent_id),
                voice_route_id=voice_entry.voice_route_id,
                intent_id=voice_entry.intent_id,
                display_route_id=voice_entry.target_display_route_id,
                target_view_id=voice_entry.target_view_id,
                target_display_id=display_entry.selected_display_id,
                target_display_role=voice_entry.target_display_role,
                target_panel_id=voice_entry.target_panel_id,
                explanation_binding_id=explainable_entry.binding_id,
                handoff_mode="display_plus_explanation",
                low_latency_required=voice_entry.low_latency_required,
                explanation_text_available=explainable_entry.explanation_text_available,
                explanation_payload_available=explainable_entry.explanation_payload_available,
                multilingual_ready=(
                    voice_entry.multilingual_ready
                    and explainable_entry.multilingual_ready
                    and display_entry.multilingual_ready
                ),
                active=voice_entry.active,
                handoff_status="ready",
                description=(
                    f"Voice display handoff for {voice_entry.intent_id} "
                    f"toward {voice_entry.target_display_role}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    low_latency_entries = sum(
        1 for entry in entries if entry.low_latency_required
    )
    explanation_ready_entries = sum(
        1
        for entry in entries
        if entry.explanation_text_available and entry.explanation_payload_available
    )
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )

    return VoiceDisplayHandoffContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        explanation_ready_entries=explanation_ready_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )


def _resolve_handoff_id(intent_id: str) -> str:
    """Resolve canonical handoff id from normalized intent id."""
    if intent_id == "intent_show_memory_001":
        return "voicehandoff_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "voicehandoff_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "voicehandoff_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")
