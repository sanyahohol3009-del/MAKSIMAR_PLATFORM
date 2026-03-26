from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    build_execution_runtime_shell_contract,
)


def test_execution_runtime_shell_contract_builds() -> None:
    """Execution runtime shell contract should build successfully."""
    shell = build_execution_runtime_shell_contract()

    assert shell.shell_id == "execution_runtime_shell"
    assert shell.total_queue_runtime_entries == 2
    assert shell.total_lease_runtime_entries == 2
    assert shell.total_scheduler_runtime_entries == 2
    assert shell.total_admission_runtime_entries == 2
    assert shell.total_degraded_runtime_entries == 2
