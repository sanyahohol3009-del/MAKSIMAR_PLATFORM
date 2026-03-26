from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_degraded_mode_panel_contract,
)


def test_degraded_mode_panel_contract_builds() -> None:
    """Degraded mode panel contract should build successfully."""
    contract = build_degraded_mode_panel_contract()

    assert contract.panel_id == "panel_degraded_mode"
    assert contract.total_entries == 4
    assert len(contract.entries) == 4


def test_degraded_mode_panel_keeps_chat_and_safety_active() -> None:
    """Degraded mode panel should preserve chat_and_safety."""
    contract = build_degraded_mode_panel_contract()

    entry = next(
        e for e in contract.entries if e.disabled_feature == "chat_and_safety"
    )

    assert entry.safety_critical is True
    assert entry.remains_active is True
