from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_jarvis_memory_locator_contract,
)


def test_jarvis_memory_locator_smoke() -> None:
    contract = build_jarvis_memory_locator_contract()

    assert contract.total_locators >= 1
    assert contract.ready_locators == contract.total_locators
    assert contract.read_only_locators == contract.total_locators
