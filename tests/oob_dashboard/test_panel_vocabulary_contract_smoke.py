from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_vocabulary_contract import (
    build_panel_vocabulary_contract,
)


def test_panel_vocabulary_contract_smoke() -> None:
    contract = build_panel_vocabulary_contract()

    assert len(contract.entries) == 8
    assert tuple(entry.panel_id for entry in contract.entries) == build_canonical_panel_ids()


def test_panel_vocabulary_contract_titles_are_present() -> None:
    contract = build_panel_vocabulary_contract()

    for entry in contract.entries:
        assert entry.title
        assert entry.description
        assert entry.panel_family
        assert entry.panel_kind


def test_panel_vocabulary_contract_priorities_are_canonical() -> None:
    contract = build_panel_vocabulary_contract()

    assert tuple(entry.display_priority for entry in contract.entries) == (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    )
