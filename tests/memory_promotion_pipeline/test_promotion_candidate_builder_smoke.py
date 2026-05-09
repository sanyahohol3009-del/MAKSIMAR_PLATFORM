from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
)


def test_promotion_candidate_builder_smoke() -> None:
    contract = build_promotion_binding_contract()

    for entry in contract.entries:
        assert entry.binding_status == "ready_for_review"
        assert entry.approval_required is True
        assert entry.auto_promotion_allowed is False
        assert entry.binding_ready is True
