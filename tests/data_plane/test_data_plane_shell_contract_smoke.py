from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    build_data_plane_shell_contract,
)


def test_data_plane_shell_contract_builds() -> None:
    """Data plane shell contract should build successfully."""
    shell = build_data_plane_shell_contract()

    assert shell.shell_id == "data_plane_shell"
    assert shell.total_ownership_entries == 2
    assert shell.total_retention_rules == 3
    assert shell.total_cleanup_rules == 3
