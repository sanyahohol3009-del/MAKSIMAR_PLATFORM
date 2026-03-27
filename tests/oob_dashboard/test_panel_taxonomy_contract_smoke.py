from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_taxonomy_contract,
)


def test_panel_taxonomy_contract_builds() -> None:
    """Panel taxonomy contract should build successfully."""
    contract = build_panel_taxonomy_contract()

    assert contract.total_entries == 19
    assert contract.unique_families == 7
    assert contract.unique_kinds == 14
    assert contract.unique_roles == 7


def test_panel_taxonomy_family_counts() -> None:
    """Panel taxonomy should expose canonical family counts."""
    contract = build_panel_taxonomy_contract()
    family_counts = {
        summary.panel_family: summary.total_entries
        for summary in contract.family_summaries
    }

    assert family_counts["foundation_status"] == 4
    assert family_counts["read_only_monitoring"] == 2
    assert family_counts["diagnostics"] == 2
    assert family_counts["interaction"] == 2
    assert family_counts["control"] == 1
    assert family_counts["execution_observability"] == 7
    assert family_counts["navigation"] == 1


def test_panel_taxonomy_role_counts() -> None:
    """Panel taxonomy should expose canonical role counts."""
    contract = build_panel_taxonomy_contract()
    role_counts = {
        summary.panel_role: summary.total_entries
        for summary in contract.role_summaries
    }

    assert role_counts["foundation_read_only"] == 4
    assert role_counts["read_only_monitoring"] == 2
    assert role_counts["diagnostics_surface"] == 2
    assert role_counts["interaction_surface"] == 2
    assert role_counts["control_surface"] == 1
    assert role_counts["execution_surface"] == 7
    assert "navigation_surface" in role_counts
    assert role_counts["navigation_surface"] == 1


def test_panel_taxonomy_kind_counts() -> None:
    """Panel taxonomy should expose canonical kind distribution."""
    contract = build_panel_taxonomy_contract()
    kind_counts = {
        summary.panel_kind: summary.total_entries
        for summary in contract.kind_summaries
    }

    assert kind_counts["status"] == 5
    assert kind_counts["summary"] == 1
    assert kind_counts["incident"] == 1
    assert kind_counts["diagnostics"] == 1
    assert kind_counts["chat"] == 1
    assert kind_counts["settings"] == 1
    assert kind_counts["gesture"] == 1
    assert kind_counts["queue"] == 1
    assert kind_counts["topology"] == 1
    assert kind_counts["mode"] == 1
    assert kind_counts["map"] == 2
    assert kind_counts["flow"] == 1
    assert kind_counts["version_control"] == 1
    assert kind_counts["navigation"] == 1
