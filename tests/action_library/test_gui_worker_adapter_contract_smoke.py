from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.gui_worker_adapter_contract import (
    build_gui_worker_adapter_contract,
)


def test_gui_worker_adapter_contract_smoke() -> None:
    contract = build_gui_worker_adapter_contract().to_read_model()

    assert contract["capability_id"] == "gui_worker"
    assert contract["risk_class"] == "risk_gate"
    assert contract["safe_direct_allowed"] is False
