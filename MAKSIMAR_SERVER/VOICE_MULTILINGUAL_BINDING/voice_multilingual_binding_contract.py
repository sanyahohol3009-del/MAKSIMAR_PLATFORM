from __future__ import annotations

from MAKSIMAR_SERVER.INTENT_NORMALIZATION import (
    build_intent_normalization_contract,
)
from MAKSIMAR_SERVER.VOICE_LATENCY_PATH import (
    build_voice_latency_path_contract,
)
from MAKSIMAR_SERVER.VOICE_MULTILINGUAL_BINDING.voice_multilingual_binding_models import (
    VoiceMultilingualBindingContract,
    VoiceMultilingualBindingEntry,
)
from MAKSIMAR_SERVER.VOICE_ROUTING import (
    build_voice_routing_contract,
)


def build_voice_multilingual_binding_contract() -> VoiceMultilingualBindingContract:
    """Build canonical voice multilingual / multiscript binding contract."""
    intent_normalization = build_intent_normalization_contract()
    voice_routing = build_voice_routing_contract()
    voice_latency_path = build_voice_latency_path_contract()

    routing_by_intent = {
        entry.intent_id: entry for entry in voice_routing.entries
    }
    path_by_intent = {
        entry.intent_id: entry for entry in voice_latency_path.entries
    }

    localized_texts_by_intent = {
        "intent_show_memory_001": (
            "show memory",
            "покажи память",
            "покажи памʼять",
            "zeige speicher",
        ),
        "intent_show_simulation_001": (
            "show simulation",
            "покажи симуляцию",
            "покажи симуляцію",
            "zeige simulation",
        ),
        "intent_show_monitoring_001": (
            "show monitoring",
            "покажи мониторинг",
            "покажи моніторинг",
            "zeige monitoring",
        ),
    }

    entries = []
    for intent_entry in intent_normalization.entries:
        routing_entry = routing_by_intent[intent_entry.intent_id]
        path_entry = path_by_intent[intent_entry.intent_id]

        entries.append(
            VoiceMultilingualBindingEntry(
                binding_id=_resolve_binding_id(intent_entry.intent_id),
                intent_id=intent_entry.intent_id,
                voice_route_id=routing_entry.voice_route_id,
                latency_path_id=path_entry.path_id,
                canonical_text=intent_entry.normalized_text,  # type: ignore[arg-type]
                supported_languages=("en", "ru", "uk", "de"),
                supported_scripts=("Latin", "Cyrillic"),
                localized_texts=localized_texts_by_intent[intent_entry.intent_id],
                low_latency_required=(
                    intent_entry.low_latency_required
                    and routing_entry.low_latency_required
                    and path_entry.low_latency_required
                ),
                explanation_required=(
                    intent_entry.explanation_required
                    and routing_entry.explanation_required
                    and path_entry.explanation_required
                ),
                multilingual_ready=(
                    intent_entry.multilingual_ready
                    and routing_entry.multilingual_ready
                    and path_entry.multilingual_ready
                ),
                multiscript_ready=True,
                active=(
                    intent_entry.active
                    and routing_entry.active
                    and path_entry.active
                ),
                binding_status="bound",
                description=(
                    f"Voice multilingual binding for {intent_entry.intent_id} "
                    f"with canonical text '{intent_entry.normalized_text}'."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    low_latency_entries = sum(
        1 for entry in entries if entry.low_latency_required
    )
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )
    multiscript_ready_entries = sum(
        1 for entry in entries if entry.multiscript_ready
    )

    return VoiceMultilingualBindingContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        multiscript_ready_entries=multiscript_ready_entries,
        entries=tuple(entries),
    )


def _resolve_binding_id(intent_id: str) -> str:
    """Resolve canonical multilingual binding id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "voicemlang_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "voicemlang_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "voicemlang_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")
