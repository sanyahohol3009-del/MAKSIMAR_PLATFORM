from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    VisualBackendEntry,
    build_visual_backend_contract,
)


def test_visual_backend_contract_builds() -> None:
    contract = build_visual_backend_contract()

    assert contract.contract_id == "visual_backend_contract_001"
    assert contract.total_entries == 3
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_visual_backend_contract_contains_expected_backend_names() -> None:
    contract = build_visual_backend_contract()

    values = tuple(
        (entry.backend_id, entry.backend_name, entry.backend_type)
        for entry in contract.entries
    )

    assert values == (
        ("visual_backend_graph_001", "react_flow_adapter_backend", "graph_backend"),
        ("visual_backend_chart_001", "echarts_adapter_backend", "chart_backend"),
        ("visual_backend_overlay_001", "internal_overlay_adapter_backend", "overlay_backend"),
    )


def test_visual_backend_entry_rejects_non_replaceable() -> None:
    with pytest.raises(
        ValueError,
        match="replaceable must remain true for canonical visual backend entries.",
    ):
        VisualBackendEntry(
            backend_id="bad_backend",
            backend_name="bad_backend_name",
            backend_type="graph_backend",
            backend_vendor_mode="optional_external_backend",
            replaceable=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid backend entry.",
        )
