from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
)


def test_promotion_archived_conflict_candidate_smoke() -> None:
    contract = build_promotion_binding_contract()

    archived_entries = [
        entry for entry in contract.entries if entry.archived_entries > 0
    ]

    assert archived_entries

    for entry in archived_entries:
        assert entry.binding_ready is True
        assert entry.approval_required is True
        assert entry.auto_promotion_allowed is False
        assert entry.read_only is True
        assert entry.binding_status == "ready_for_review"
