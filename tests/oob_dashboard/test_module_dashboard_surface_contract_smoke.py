from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_dashboard_surface_contract import (
    ModuleDashboardSurfaceEntry,
    build_module_dashboard_surface_contract,
)


def test_module_dashboard_surface_contract_builds() -> None:
    contract = build_module_dashboard_surface_contract()
    assert contract.contract_id == "module_dashboard_surface_contract_001"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_dashboard_surface_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical module dashboard surface entries.",
    ):
        ModuleDashboardSurfaceEntry(
            surface_entry_id="bad_surface",
            module_id="module_manifest_001",
            surface_id="bad_surface",
            workspace_id="workspace_foundation_monitoring",
            surface_kind="foundation_dashboard_surface",
            operator_visible=True,
            truth_bound=False,
            description="Invalid surface entry.",
        )
