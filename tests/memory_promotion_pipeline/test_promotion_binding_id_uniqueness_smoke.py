from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
)


def test_promotion_binding_id_uniqueness_smoke() -> None:
    contract = build_promotion_binding_contract()

    binding_ids = tuple(entry.promotion_binding_id for entry in contract.entries)

    assert len(binding_ids) == len(set(binding_ids))
    assert contract.ready_bindings == contract.total_bindings
