from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_input_contract,
)


def test_input_contract_builds() -> None:
    contract = build_dashboard_input_contract()

    assert len(contract.capabilities) >= 1
    assert len(contract.supported_actions) >= 1


def test_input_types_present() -> None:
    contract = build_dashboard_input_contract()

    types = {c.input_type for c in contract.capabilities}

    assert "mouse" in types
    assert "keyboard" in types
    assert "voice" in types
    assert "gesture" in types
