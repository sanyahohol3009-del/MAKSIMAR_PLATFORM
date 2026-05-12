from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import (
    build_memory_acceptance_contract,
    build_memory_release_preview,
    build_memory_write_safety_policy,
)


def test_memory_no_duplicate_write_smoke() -> None:
    contract = build_memory_acceptance_contract()
    policy = build_memory_write_safety_policy()
    preview = build_memory_release_preview()

    assert contract.duplicate_write_allowed is False
    assert policy.duplicate_write_allowed is False
    assert preview["duplicate_write_allowed"] is False
