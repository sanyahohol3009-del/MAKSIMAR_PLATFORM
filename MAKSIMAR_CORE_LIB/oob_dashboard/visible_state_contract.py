from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.final_visible_screen_state_contract import (
    build_final_visible_screen_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visible_state_models import (
    VisibleStateContract,
    VisibleStateEntry,
)


def build_visible_state_contract() -> VisibleStateContract:
    """Build canonical visible state contract."""
    final_visible_screen_state_contract = build_final_visible_screen_state_contract()

    interaction_targets = {"display_operator_interaction"}

    entries = tuple(
        VisibleStateEntry(
            visible_state_id=f"visible_state_{index:03d}",
            display_target_id=entry.display_target_id,
            workspace_id=entry.workspace_id,
            visible_state_state="visible_state_ready",
            visible_state_class=(
                "interaction_visible_state"
                if entry.display_target_id in interaction_targets
                else "foundation_visible_state"
            ),
            visible_state_mode=(
                "assembled_interaction_visible_state"
                if entry.display_target_id in interaction_targets
                else "assembled_foundation_visible_state"
            ),
            final_visible_screen_state_ready=True,
            operator_visible=entry.operator_visible,
            truth_bound=entry.truth_bound,
            description=(
                "Canonical visible state entry for "
                f"{entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(
            final_visible_screen_state_contract.entries,
            start=1,
        )
    )

    return VisibleStateContract(
        contract_id="visible_state_contract_001",
        total_entries=len(entries),
        foundation_visible_entries=sum(
            1
            for entry in entries
            if entry.visible_state_class == "foundation_visible_state"
        ),
        interaction_visible_entries=sum(
            1
            for entry in entries
            if entry.visible_state_class == "interaction_visible_state"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
