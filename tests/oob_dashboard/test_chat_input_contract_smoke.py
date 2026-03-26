from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_chat_input_contract,
)


def test_chat_input_contract_builds() -> None:
    """Chat-input contract should build successfully."""
    contract = build_dashboard_chat_input_contract()

    assert len(contract.bindings) == 3
    assert len(contract.output_modes) == 3


def test_chat_input_contract_modes_present() -> None:
    """Chat-input contract should expose text, voice and gesture modes."""
    contract = build_dashboard_chat_input_contract()

    modes = {binding.input_mode for binding in contract.bindings}

    assert "text" in modes
    assert "voice" in modes
    assert "gesture" in modes
