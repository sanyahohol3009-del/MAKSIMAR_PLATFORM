from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
    build_promotion_summary,
)


def test_promotion_governance_binding_ready_smoke() -> None:
    contract = build_promotion_binding_contract()
    summary = build_promotion_summary()

    assert contract.ready_bindings == contract.total_bindings
    assert summary["summary_ready"] is True
