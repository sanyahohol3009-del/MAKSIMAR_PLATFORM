from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


def test_panel_metadata_contract_smoke() -> None:
    contract = build_panel_metadata_contract()

    assert len(contract.entries) == 8
    assert tuple(entry.panel_id for entry in contract.entries) == build_canonical_panel_ids()


def test_panel_metadata_contract_titles_and_labels_are_present() -> None:
    contract = build_panel_metadata_contract()

    for entry in contract.entries:
        assert entry.title
        assert entry.short_label
        assert entry.description
        assert entry.panel_family
        assert entry.panel_kind
