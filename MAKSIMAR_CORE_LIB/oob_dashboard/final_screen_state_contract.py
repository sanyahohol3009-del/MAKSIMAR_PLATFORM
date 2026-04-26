from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.final_screen_state_models import (
    FinalScreenStateContract,
    FinalScreenStateEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.final_visible_screen_state_contract import (
    build_final_visible_screen_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_runtime_contract import (
    build_presentation_bundle_runtime_contract,
)


def build_final_screen_state_contract() -> FinalScreenStateContract:
    """Build canonical final screen state contract."""
    final_visible_screen_state_contract = build_final_visible_screen_state_contract()
    presentation_bundle_runtime_contract = build_presentation_bundle_runtime_contract()

    final_visible_screen_state_ready = bool(final_visible_screen_state_contract.entries)
    presentation_bundle_runtime_ready = bool(
        presentation_bundle_runtime_contract.entries
    )
    interaction_targets = {"display_operator_interaction"}

    entries = tuple(
        FinalScreenStateEntry(
            final_screen_state_id=f"final_screen_state_{index:03d}",
            display_target_id=entry.display_target_id,
            workspace_id=entry.workspace_id,
            final_screen_state_state="final_screen_state_ready",
            final_screen_state_class=(
                "interaction_final_screen_state"
                if entry.display_target_id in interaction_targets
                else "foundation_final_screen_state"
            ),
            final_screen_state_mode=(
                "assembled_interaction_final_screen_state"
                if entry.display_target_id in interaction_targets
                else "assembled_foundation_final_screen_state"
            ),
            final_visible_screen_state_ready=final_visible_screen_state_ready,
            presentation_bundle_runtime_ready=presentation_bundle_runtime_ready,
            operator_visible=entry.operator_visible,
            truth_bound=entry.truth_bound,
            description=(
                "Canonical final screen state entry for "
                f"{entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(
            final_visible_screen_state_contract.entries,
            start=1,
        )
    )

    return FinalScreenStateContract(
        contract_id="final_screen_state_contract_001",
        total_entries=len(entries),
        foundation_final_entries=sum(
            1
            for entry in entries
            if entry.final_screen_state_class == "foundation_final_screen_state"
        ),
        interaction_final_entries=sum(
            1
            for entry in entries
            if entry.final_screen_state_class == "interaction_final_screen_state"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
