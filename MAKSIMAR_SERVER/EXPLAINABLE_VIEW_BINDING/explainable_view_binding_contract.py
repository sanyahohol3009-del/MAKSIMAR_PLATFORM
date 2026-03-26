from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_models import (
    ExplainableViewBindingContract,
    ExplainableViewBindingEntry,
)


def build_explainable_view_binding_contract() -> ExplainableViewBindingContract:
    """Build canonical explainable view binding contract."""
    display_topology = build_display_topology_contract()
    display_orchestration = build_display_orchestration_contract()

    display_by_role = {
        entry.display_role: entry for entry in display_topology.entries
    }

    entries = []
    for orchestration_entry in display_orchestration.entries:
        display_entry = display_by_role[orchestration_entry.selected_display_role]

        entries.append(
            ExplainableViewBindingEntry(
                binding_id=f"explainbind_{orchestration_entry.route_request_id}",
                view_id=orchestration_entry.resolved_view_id,
                panel_id=orchestration_entry.selected_panel_id,
                display_id=display_entry.display_id,
                display_role=display_entry.display_role,
                summary_mode="summary_available",
                reasoning_mode="reasoning_payload_available",
                safety_mode="safety_note_available",
                multilingual_ready=display_entry.supports_multilingual_rendering,
                explanation_text_available=orchestration_entry.explanation_required,
                explanation_payload_available=orchestration_entry.registry_routed,
                binding_status="bound",
                description=(
                    f"Explainable view binding for {orchestration_entry.resolved_view_id} "
                    f"on display role {display_entry.display_role}."
                ),
            )
        )

    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )
    explanation_text_entries = sum(
        1 for entry in entries if entry.explanation_text_available
    )
    explanation_payload_entries = sum(
        1 for entry in entries if entry.explanation_payload_available
    )

    return ExplainableViewBindingContract(
        total_entries=len(entries),
        multilingual_ready_entries=multilingual_ready_entries,
        explanation_text_entries=explanation_text_entries,
        explanation_payload_entries=explanation_payload_entries,
        entries=tuple(entries),
    )
