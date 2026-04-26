from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.chart_render_adapter_contract import (
    ChartRenderAdapterEntry,
    build_chart_render_adapter_contract,
)


def test_chart_render_adapter_contract_builds() -> None:
    contract = build_chart_render_adapter_contract()

    assert contract.contract_id == "chart_render_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_chart_render_adapter_contract_contains_expected_targets() -> None:
    contract = build_chart_render_adapter_contract()

    values = tuple(
        (entry.adapter_entry_id, entry.adapter_target, entry.backend_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "chart_render_adapter_001",
            "node_resources_chart_projection",
            "visual_backend_chart_001",
        ),
        (
            "chart_render_adapter_002",
            "export_validation_assets_chart_projection",
            "visual_backend_chart_001",
        ),
        (
            "chart_render_adapter_003",
            "security_telemetry_chart_projection",
            "visual_backend_chart_001",
        ),
    )


def test_chart_render_adapter_entry_rejects_vendor_series_leakage() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_series_exposed must remain false for canonical chart render adapter entries.",
    ):
        ChartRenderAdapterEntry(
            adapter_entry_id="bad_chart_adapter",
            backend_id="visual_backend_chart_001",
            adapter_target="bad_chart_target",
            adapter_mode="canonical_to_chart_backend",
            canonical_id_preserved=True,
            vendor_series_exposed=True,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid chart adapter entry.",
        )
