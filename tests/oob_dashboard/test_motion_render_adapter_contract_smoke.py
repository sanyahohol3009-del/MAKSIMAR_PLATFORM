from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.motion_render_adapter_contract import (
    MotionRenderAdapterEntry,
    build_motion_render_adapter_contract,
)


def test_motion_render_adapter_contract_builds() -> None:
    contract = build_motion_render_adapter_contract()

    assert contract.contract_id == "motion_render_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_motion_render_adapter_contract_contains_expected_targets() -> None:
    contract = build_motion_render_adapter_contract()

    values = tuple(
        (entry.adapter_entry_id, entry.adapter_target, entry.motion_policy_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "motion_render_adapter_001",
            "hud_transition_projection",
            "motion_policy_hud_transition",
        ),
        (
            "motion_render_adapter_002",
            "status_pulse_projection",
            "motion_policy_status_pulse",
        ),
        (
            "motion_render_adapter_003",
            "panel_reveal_projection",
            "motion_policy_panel_reveal",
        ),
    )


def test_motion_render_adapter_entry_rejects_vendor_motion_leakage() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_motion_exposed must remain false for canonical motion render adapter entries.",
    ):
        MotionRenderAdapterEntry(
            adapter_entry_id="bad_motion_adapter",
            adapter_target="bad_motion_target",
            adapter_mode="canonical_to_motion_backend",
            motion_policy_id="motion_policy_bad",
            canonical_id_preserved=True,
            vendor_motion_exposed=True,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid motion adapter entry.",
        )
