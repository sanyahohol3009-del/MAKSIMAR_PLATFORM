from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_runtime import (
    build_worker_runtime_shell_contract,
)


def test_worker_runtime_shell_contract_builds() -> None:
    """Worker runtime shell contract should build successfully."""
    shell = build_worker_runtime_shell_contract()

    assert shell.shell_id == "worker_runtime_shell"
    assert shell.total_health_entries == 3
    assert shell.total_load_entries == 3
