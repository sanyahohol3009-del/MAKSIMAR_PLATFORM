from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_deep_execution_observability_shell_contract,
)


def test_deep_execution_observability_shell_contract_builds() -> None:
    """Deep execution observability shell should build successfully."""
    shell = build_deep_execution_observability_shell_contract()

    assert shell.shell_id == "execution_observability_deep_shell"
    assert shell.total_queue_metrics == 2
    assert shell.total_lease_metrics == 2
    assert shell.total_pressure_metrics == 3
    assert shell.total_worker_saturation_metrics == 3
