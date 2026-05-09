from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_contract,
    build_storage_registry_flow_preview,
    build_storage_registry_preview,
    validate_storage_registry_ready,
)


def test_storage_registry_ready_smoke() -> None:
    contract = build_storage_registry_contract()
    preview = build_storage_registry_preview()
    flow = build_storage_registry_flow_preview()

    assert validate_storage_registry_ready(contract) is True
    assert preview["preview_ready"] is True
    assert flow["flow_ready"] is True
    assert contract.total_entries == preview["total_entries"]
