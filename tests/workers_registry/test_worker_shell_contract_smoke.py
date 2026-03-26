from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    build_worker_registry_shell_contract,
)


def test_worker_registry_shell_contract_builds() -> None:
    shell = build_worker_registry_shell_contract()

    assert shell.shell_id == "worker_registry_shell"
    assert shell.total_workers == 3
    assert shell.total_capabilities == 3
    assert shell.total_io_entries == 3
