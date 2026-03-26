from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    build_execution_control_shell_contract,
)


def test_execution_control_shell_contract_builds() -> None:
    """Execution control shell contract should build successfully."""
    shell = build_execution_control_shell_contract()

    assert shell.shell_id == "execution_control_shell"
    assert shell.total_tasks == 10
    assert shell.total_queues == 1
    assert shell.total_leases == 1
    assert shell.total_schedulers == 1


def test_execution_control_shell_contract_counts_routes_and_admission() -> None:
    """Execution control shell contract should expose routing and admission counts."""
    shell = build_execution_control_shell_contract()

    assert shell.total_admission_decisions == 2
    assert shell.total_routes == 2
    assert shell.degraded_mode_active is False
