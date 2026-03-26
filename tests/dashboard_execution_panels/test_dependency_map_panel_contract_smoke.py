from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dependency_map_panel_contract,
)


def test_dependency_map_panel_contract_builds() -> None:
    """Dependency map panel contract should build successfully."""
    contract = build_dependency_map_panel_contract()

    assert contract.panel_id == "panel_dependency_map"
    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_dependency_map_panel_contains_execution_dependency_path() -> None:
    """Dependency map panel should expose execution dependency path."""
    contract = build_dependency_map_panel_contract()

    pairs = {
        (entry.upstream_module_id, entry.downstream_module_id)
        for entry in contract.entries
    }

    assert ("control_plane", "execution_control") in pairs
    assert ("execution_control", "execution_observability") in pairs
