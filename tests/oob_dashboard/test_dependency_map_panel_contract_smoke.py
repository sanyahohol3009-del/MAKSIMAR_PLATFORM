from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_contract import (
    build_dependency_map_panel_contract,
)


def test_dependency_map_panel_contract_builds() -> None:
    contract = build_dependency_map_panel_contract()

    assert contract.panel_id == "panel_dependency_map"
    assert contract.total_entries == 3
    assert contract.operator_visible is True


def test_dependency_map_panel_contract_contains_expected_dependencies() -> None:
    contract = build_dependency_map_panel_contract()

    dependencies = tuple(
        (
            entry.upstream_module_id,
            entry.downstream_module_id,
            entry.dependency_kind,
        )
        for entry in contract.entries
    )

    assert dependencies == (
        ("control_plane", "execution_control", "execution_dependency"),
        ("execution_control", "execution_observability", "execution_dependency"),
        ("execution_observability", "oob_dashboard", "projection_dependency"),
    )
