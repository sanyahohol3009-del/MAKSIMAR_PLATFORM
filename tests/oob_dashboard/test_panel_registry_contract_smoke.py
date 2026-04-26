from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_panel_registry_contract,
)


def test_panel_registry_contract_smoke() -> None:
    contract = build_panel_registry_contract()

    assert len(contract.entries) == 8
    assert tuple(entry.panel_id for entry in contract.entries) == build_canonical_panel_ids()


def test_panel_registry_contract_requires_source_binding_and_visibility_policy() -> None:
    contract = build_panel_registry_contract()

    for entry in contract.entries:
        assert entry.source_binding_required is True
        assert entry.visibility_policy_required is True
