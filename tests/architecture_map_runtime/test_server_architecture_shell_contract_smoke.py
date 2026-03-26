from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_server_architecture_map_shell_contract,
)


def test_server_architecture_map_shell_contract_builds() -> None:
    """Server architecture map shell contract should build successfully."""
    shell = build_server_architecture_map_shell_contract()

    assert shell.shell_id == "server_architecture_map_shell"
    assert shell.total_module_views == 3
    assert shell.total_dependency_views == 3
    assert shell.total_flow_views == 5
