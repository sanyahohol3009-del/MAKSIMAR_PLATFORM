from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.degraded_mode_panel_contract import (
    build_degraded_mode_panel_contract,
)


def test_degraded_mode_panel_contract_builds() -> None:
    contract = build_degraded_mode_panel_contract()

    assert contract.panel_id == "panel_degraded_mode"
    assert contract.total_entries == 4
    assert contract.operator_visible is True


def test_degraded_mode_panel_contract_contains_expected_entries() -> None:
    contract = build_degraded_mode_panel_contract()

    features = tuple(entry.disabled_feature for entry in contract.entries)
    assert features == (
        "heavy_simulation",
        "chat_and_safety",
        "background_analytics",
        "premium_visualization",
    )

    chat_entry = next(
        entry for entry in contract.entries if entry.disabled_feature == "chat_and_safety"
    )
    assert chat_entry.degradation_status == "kept_active"
    assert chat_entry.fallback_mode == "read_only_and_guarded"
    assert chat_entry.safety_critical is True
    assert chat_entry.remains_active is True
