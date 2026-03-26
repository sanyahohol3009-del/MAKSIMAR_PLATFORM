from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_shell_contract,
)


def test_dashboard_shell_contract_builds() -> None:
    """Dashboard shell contract should build successfully."""
    shell = build_dashboard_shell_contract()

    assert shell.shell_id == "oob_dashboard_shell"
    assert shell.total_panels == 7
    assert shell.total_displays == 3
    assert shell.total_feedback_items == 4


def test_dashboard_shell_contract_has_active_panel() -> None:
    """Dashboard shell contract should expose active panel and consistency status."""
    shell = build_dashboard_shell_contract()

    assert shell.active_panel_id == "panel_consistency"
    assert shell.consistency_status == "consistent"
