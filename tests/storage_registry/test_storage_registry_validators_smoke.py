from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_contract,
    validate_storage_registry_ready,
)


def test_storage_registry_validators_smoke() -> None:
    contract = build_storage_registry_contract()

    assert validate_storage_registry_ready(contract) is True
