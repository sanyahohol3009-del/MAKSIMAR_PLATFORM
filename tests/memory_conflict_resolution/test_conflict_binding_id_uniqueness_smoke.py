from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
)


def test_conflict_binding_id_uniqueness_smoke() -> None:
    contract = build_conflict_binding_contract()

    binding_ids = tuple(entry.conflict_binding_id for entry in contract.entries)

    assert len(binding_ids) == len(set(binding_ids))
