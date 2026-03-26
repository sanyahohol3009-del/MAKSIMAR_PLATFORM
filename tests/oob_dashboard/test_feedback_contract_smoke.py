from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_feedback_contract,
)


def test_feedback_contract_builds() -> None:
    """Feedback contract should build successfully."""
    contract = build_dashboard_feedback_contract()

    assert contract.total_items == 4
    assert len(contract.items) == 4


def test_feedback_contract_contains_root_cause_data() -> None:
    """Feedback contract should contain source and probable location."""
    contract = build_dashboard_feedback_contract()

    assert contract.items[0].source_name != ""
    assert contract.items[0].probable_location != ""
