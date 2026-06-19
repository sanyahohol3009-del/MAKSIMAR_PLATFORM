from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.browser_worker_adapter_contract import (
    build_browser_worker_adapter_contract,
)


def test_browser_worker_adapter_contract_smoke() -> None:
    contract = build_browser_worker_adapter_contract().to_read_model()

    assert contract["capability_id"] == "browser_worker"
    assert contract["risk_class"] == "safe_direct"
    assert contract["requires_verified_owner"] is True
    assert contract["safe_direct_allowed"] is True
