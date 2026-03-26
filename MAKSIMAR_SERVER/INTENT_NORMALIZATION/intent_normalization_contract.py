from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_layer import (
    build_voice_command_contract,
)
from MAKSIMAR_SERVER.INTENT_NORMALIZATION.intent_normalization_models import (
    IntentNormalizationContract,
    NormalizedIntentEntry,
)


def _resolve_target_domain(command_intent: str) -> str:
    """Resolve canonical target domain from command intent."""
    if command_intent == "show_memory":
        return "memory"
    if command_intent == "show_simulation":
        return "simulation"
    if command_intent == "show_monitoring":
        return "monitoring"
    raise ValueError(f"Unsupported command_intent: {command_intent}")


def _resolve_normalized_text(command_intent: str) -> str:
    """Resolve canonical normalized text from command intent."""
    if command_intent == "show_memory":
        return "show memory"
    if command_intent == "show_simulation":
        return "show simulation"
    if command_intent == "show_monitoring":
        return "show monitoring"
    raise ValueError(f"Unsupported command_intent: {command_intent}")


def build_intent_normalization_contract() -> IntentNormalizationContract:
    """Build canonical normalized intent contract."""
    voice_command_contract = build_voice_command_contract()

    entries = []
    for voice_entry in voice_command_contract.entries:
        entries.append(
            NormalizedIntentEntry(
                intent_id=f"intent_{voice_entry.command_intent}_001",
                intent_source="voice",
                source_command_id=voice_entry.command_id,
                intent_kind="display_request",
                target_domain=_resolve_target_domain(voice_entry.command_intent),  # type: ignore[arg-type]
                target_action="show",
                target_view_id=voice_entry.target_view_id,
                target_display_role=voice_entry.target_display_role,
                normalized_text=_resolve_normalized_text(voice_entry.command_intent),
                confidence_band="high",
                low_latency_required=voice_entry.low_latency_required,
                explanation_required=voice_entry.explanation_required,
                multilingual_ready=voice_entry.multilingual_ready,
                active=voice_entry.active,
                normalization_status="normalized",
                description=(
                    f"Normalized platform intent for {voice_entry.command_id} "
                    f"toward {voice_entry.target_display_role}."
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

    return IntentNormalizationContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        explanation_required_entries=explanation_required_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )
