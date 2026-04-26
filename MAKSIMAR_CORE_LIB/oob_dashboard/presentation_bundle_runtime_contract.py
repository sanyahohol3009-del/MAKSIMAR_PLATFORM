from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_models import (
    PresentationBundleRuntimeContract,
    PresentationBundleRuntimeEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_contract import (
    build_presentation_bundle_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visible_state_contract import (
    build_visible_state_contract,
)


def build_presentation_bundle_runtime_contract() -> PresentationBundleRuntimeContract:
    """Build canonical presentation-bundle runtime contract."""
    presentation_bundle_contract = build_presentation_bundle_contract()
    visible_state_contract = build_visible_state_contract()

    visible_state_ready = bool(visible_state_contract.entries)
    interaction_targets = {"display_operator_interaction"}

    entries = tuple(
        PresentationBundleRuntimeEntry(
            presentation_bundle_runtime_id=f"presentation_bundle_runtime_{index:03d}",
            display_target_id=entry.display_target_id,
            workspace_id=entry.workspace_id,
            presentation_bundle_runtime_state="presentation_bundle_runtime_ready",
            presentation_bundle_runtime_class=(
                "interaction_presentation_runtime"
                if entry.display_target_id in interaction_targets
                else "foundation_presentation_runtime"
            ),
            presentation_bundle_runtime_mode=(
                "assembled_interaction_presentation_runtime"
                if entry.display_target_id in interaction_targets
                else "assembled_foundation_presentation_runtime"
            ),
            visible_state_ready=visible_state_ready,
            operator_visible=entry.operator_visible,
            truth_bound=entry.truth_bound,
            description=(
                "Canonical presentation-bundle runtime entry for "
                f"{entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(
            presentation_bundle_contract.entries,
            start=1,
        )
    )

    return PresentationBundleRuntimeContract(
        contract_id="presentation_bundle_runtime_contract_001",
        total_entries=len(entries),
        foundation_runtime_entries=sum(
            1
            for entry in entries
            if entry.presentation_bundle_runtime_class == "foundation_presentation_runtime"
        ),
        interaction_runtime_entries=sum(
            1
            for entry in entries
            if entry.presentation_bundle_runtime_class == "interaction_presentation_runtime"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
