from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.cli_worker_adapter_contract import (
    build_cli_worker_adapter_contract,
)


def test_cli_worker_adapter_contract_smoke() -> None:
    contract = build_cli_worker_adapter_contract().to_read_model()

    assert contract["capability_id"] == "cli_worker"
    assert contract["risk_class"] == "risk_gate"
    assert "shell_command" in contract["side_effects"]
