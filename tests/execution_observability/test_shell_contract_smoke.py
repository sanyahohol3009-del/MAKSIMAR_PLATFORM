from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_observability_shell_contract,
)


def test_execution_observability_shell_contract_builds() -> None:
    shell = build_execution_observability_shell_contract()

    assert shell.shell_id == "execution_observability_shell"
    assert shell.total_metrics == 5
    assert shell.total_summary_lines == 5
    assert shell.total_alerts == 3
    assert shell.total_incidents == 3
    assert shell.total_traces == 2


def test_execution_observability_shell_contract_has_valid_status() -> None:
    shell = build_execution_observability_shell_contract()

    assert shell.overall_status in {"ok", "warning", "critical"}
