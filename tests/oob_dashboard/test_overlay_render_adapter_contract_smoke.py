from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.overlay_render_adapter_contract import (
    OverlayRenderAdapterEntry,
    build_overlay_render_adapter_contract,
)


def test_overlay_render_adapter_contract_builds() -> None:
    contract = build_overlay_render_adapter_contract()

    assert contract.contract_id == "overlay_render_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_overlay_render_adapter_contract_contains_expected_targets() -> None:
    contract = build_overlay_render_adapter_contract()

    values = tuple(
        (entry.adapter_entry_id, entry.adapter_target, entry.backend_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "overlay_render_adapter_001",
            "signal_overlay_projection",
            "visual_backend_overlay_001",
        ),
        (
            "overlay_render_adapter_002",
            "topology_overlay_projection",
            "visual_backend_overlay_001",
        ),
        (
            "overlay_render_adapter_003",
            "explainability_overlay_projection",
            "visual_backend_overlay_001",
        ),
    )


def test_overlay_render_adapter_entry_rejects_vendor_overlay_leakage() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_overlay_exposed must remain false for canonical overlay render adapter entries.",
    ):
        OverlayRenderAdapterEntry(
            adapter_entry_id="bad_overlay_adapter",
            backend_id="visual_backend_overlay_001",
            adapter_target="bad_overlay_target",
            adapter_mode="canonical_to_overlay_backend",
            canonical_id_preserved=True,
            vendor_overlay_exposed=True,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid overlay adapter entry.",
        )
