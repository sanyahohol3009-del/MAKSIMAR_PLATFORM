from __future__ import annotations

from MAKSIMAR_SERVER.INTENT_NORMALIZATION import (
    build_intent_normalization_contract,
)
from MAKSIMAR_SERVER.VOICE_DISPLAY_HANDOFF import (
    build_voice_display_handoff_contract,
)
from MAKSIMAR_SERVER.VOICE_EXECUTION_HANDOFF import (
    build_voice_execution_handoff_contract,
)
from MAKSIMAR_SERVER.VOICE_LATENCY_PATH.voice_latency_path_models import (
    VoiceLatencyPathContract,
    VoiceLatencyPathEntry,
)
from MAKSIMAR_SERVER.VOICE_ROUTING import (
    build_voice_routing_contract,
)


def build_voice_latency_path_contract() -> VoiceLatencyPathContract:
    """Build canonical voice latency path contract."""
    intent_normalization = build_intent_normalization_contract()
    voice_routing = build_voice_routing_contract()
    display_handoff = build_voice_display_handoff_contract()
    execution_handoff = build_voice_execution_handoff_contract()

    routing_by_intent = {
        entry.intent_id: entry for entry in voice_routing.entries
    }
    display_handoff_by_intent = {
        entry.intent_id: entry for entry in display_handoff.entries
    }
    execution_handoff_by_intent = {
        entry.intent_id: entry for entry in execution_handoff.entries
    }

    entries = []
    for intent_entry in intent_normalization.entries:
        routing_entry = routing_by_intent[intent_entry.intent_id]
        display_entry = display_handoff_by_intent[intent_entry.intent_id]
        execution_entry = execution_handoff_by_intent[intent_entry.intent_id]

        entries.append(
            VoiceLatencyPathEntry(
                path_id=_resolve_path_id(intent_entry.intent_id),
                intent_id=intent_entry.intent_id,
                latency_class="near_instant",
                stage_ids=(
                    "voice_input_stage",
                    "intent_normalization_stage",
                    "voice_routing_stage",
                    "display_handoff_stage",
                    "execution_handoff_stage",
                ),
                source_command_id=intent_entry.source_command_id,
                normalization_binding_id=intent_entry.intent_id,
                voice_route_id=routing_entry.voice_route_id,
                display_handoff_id=display_entry.handoff_id,
                execution_handoff_id=execution_entry.handoff_id,
                low_latency_required=(
                    intent_entry.low_latency_required
                    and routing_entry.low_latency_required
                    and display_entry.low_latency_required
                    and execution_entry.low_latency_required
                ),
                explanation_required=(
                    intent_entry.explanation_required
                    and routing_entry.explanation_required
                    and execution_entry.explanation_required
                ),
                multilingual_ready=(
                    intent_entry.multilingual_ready
                    and routing_entry.multilingual_ready
                    and display_entry.multilingual_ready
                ),
                active=(
                    intent_entry.active
                    and routing_entry.active
                    and display_entry.active
                    and execution_entry.active
                ),
                path_status="ready",
                description=(
                    f"Canonical low-latency voice path for {intent_entry.intent_id} "
                    f"across normalization, routing, display, and execution handoff."
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

    return VoiceLatencyPathContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        explanation_required_entries=explanation_required_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )


def _resolve_path_id(intent_id: str) -> str:
    """Resolve canonical latency path id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "latencypath_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "latencypath_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "latencypath_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")
