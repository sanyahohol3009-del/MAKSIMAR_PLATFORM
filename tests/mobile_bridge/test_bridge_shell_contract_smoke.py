from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge import (
    build_mobile_bridge_shell_contract,
)


def test_mobile_bridge_shell_contract_builds() -> None:
    """Mobile bridge shell contract should build successfully."""
    shell = build_mobile_bridge_shell_contract()

    assert shell.shell_id == "mobile_bridge_shell"
    assert shell.total_requests == 2
    assert shell.total_envelopes == 2
    assert shell.total_results == 2


def test_mobile_bridge_shell_contract_is_core_safe() -> None:
    """Mobile bridge shell should stay core-safe and mobile-lightweight."""
    shell = build_mobile_bridge_shell_contract()

    assert shell.core_write_allowed is False
    assert shell.heavy_execution_allowed_on_mobile is False
