from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_degraded_mode_contract,
)


def test_degraded_mode_contract_builds() -> None:
    """Degraded mode contract should build successfully."""
    contract = build_degraded_mode_contract()

    assert contract.total_rules == 4
    assert len(contract.rules) == 4


def test_degraded_mode_keeps_chat_and_safety_active() -> None:
    """Degraded mode contract should preserve chat_and_safety."""
    contract = build_degraded_mode_contract()

    rule = next(
        r for r in contract.rules if r.disabled_feature == "chat_and_safety"
    )

    assert rule.safety_critical is True
    assert rule.remains_active is True
