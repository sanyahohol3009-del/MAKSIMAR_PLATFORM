from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_runtime_observability_shell_contract,
)


def test_observability_shell_contract_builds() -> None:
    """Runtime observability shell contract should build successfully."""
    shell = build_runtime_observability_shell_contract()

    assert shell.shell_id == "runtime_observability_shell"
    assert shell.total_metrics == 5
    assert shell.total_spans == 3
    assert shell.total_log_records == 3
    assert shell.total_config_entries == 5
    assert shell.total_slo_indicators == 3


def test_observability_shell_contract_has_status() -> None:
    """Runtime observability shell contract should expose valid status."""
    shell = build_runtime_observability_shell_contract()

    assert shell.overall_status in {"ok", "warning"}
