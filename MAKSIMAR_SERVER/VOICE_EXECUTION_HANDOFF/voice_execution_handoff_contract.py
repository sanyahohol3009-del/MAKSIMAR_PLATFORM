from __future__ import annotations

from MAKSIMAR_SERVER.VOICE_DISPLAY_HANDOFF import (
    build_voice_display_handoff_contract,
)
from MAKSIMAR_SERVER.VOICE_EXECUTION_HANDOFF.voice_execution_handoff_models import (
    VoiceExecutionHandoffContract,
    VoiceExecutionHandoffEntry,
)


def build_voice_execution_handoff_contract() -> VoiceExecutionHandoffContract:
    """Build canonical voice execution handoff contract."""
    display_handoff = build_voice_display_handoff_contract()

    entries = []
    for handoff_entry in display_handoff.entries:
        entries.append(
            VoiceExecutionHandoffEntry(
                handoff_id=_resolve_execution_handoff_id(handoff_entry.intent_id),
                intent_id=handoff_entry.intent_id,
                display_handoff_id=handoff_entry.handoff_id,
                intent_kind="display_request",
                task_class=_resolve_task_class(handoff_entry.intent_id),  # type: ignore[arg-type]
                payload_class="small_control",
                policy_rule_id=_resolve_policy_rule_id(handoff_entry.intent_id),
                validation_request_id=_resolve_validation_request_id(
                    handoff_entry.intent_id
                ),
                resolved_validation_tier="L1_HEADER",
                admission_decision="accept",
                pressure_level="normal",
                pressure_entry_id=_resolve_pressure_entry_id(handoff_entry.intent_id),
                low_latency_required=handoff_entry.low_latency_required,
                explanation_required=handoff_entry.explanation_text_available,
                policy_compatible=True,
                active=handoff_entry.active,
                handoff_mode="validation_policy_admission_handoff",
                handoff_status="ready",
                description=(
                    f"Voice execution handoff for {handoff_entry.intent_id} "
                    f"into validation/policy/admission spine."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    low_latency_entries = sum(
        1 for entry in entries if entry.low_latency_required
    )
    policy_compatible_entries = sum(
        1 for entry in entries if entry.policy_compatible
    )
    ready_entries = sum(
        1 for entry in entries if entry.handoff_status == "ready"
    )

    return VoiceExecutionHandoffContract(
        total_entries=len(entries),
        active_entries=active_entries,
        low_latency_entries=low_latency_entries,
        policy_compatible_entries=policy_compatible_entries,
        ready_entries=ready_entries,
        entries=tuple(entries),
    )


def _resolve_execution_handoff_id(intent_id: str) -> str:
    """Resolve canonical execution handoff id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "voiceexec_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "voiceexec_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "voiceexec_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_task_class(intent_id: str) -> str:
    """Resolve task_class from intent id."""
    if intent_id == "intent_show_memory_001":
        return "chat_request"
    if intent_id == "intent_show_simulation_001":
        return "simulation_request"
    if intent_id == "intent_show_monitoring_001":
        return "chat_request"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_policy_rule_id(intent_id: str) -> str:
    """Resolve policy rule id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "policy_chat_request_small_control"
    if intent_id == "intent_show_simulation_001":
        return "policy_simulation_request_small_control"
    if intent_id == "intent_show_monitoring_001":
        return "policy_chat_request_small_control"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_validation_request_id(intent_id: str) -> str:
    """Resolve validation request id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "valreq_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "valreq_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "valreq_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")


def _resolve_pressure_entry_id(intent_id: str) -> str:
    """Resolve pressure entry id from intent id."""
    if intent_id == "intent_show_memory_001":
        return "pressureentry_show_memory_001"
    if intent_id == "intent_show_simulation_001":
        return "pressureentry_show_simulation_001"
    if intent_id == "intent_show_monitoring_001":
        return "pressureentry_show_monitoring_001"
    raise ValueError(f"Unsupported intent_id: {intent_id}")
