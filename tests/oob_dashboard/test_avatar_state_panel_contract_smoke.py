from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.avatar_state_panel_contract import (
    build_avatar_state_panel_contract,
)


def test_avatar_state_panel_contract_builds() -> None:
    contract = build_avatar_state_panel_contract()

    assert contract.panel_id == "panel_avatar_state"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_avatar_state_panel_contract_contains_expected_entries() -> None:
    contract = build_avatar_state_panel_contract()

    states = tuple(
        (entry.avatar_profile_id, entry.persona_mode, entry.consent_state)
        for entry in contract.entries
    )

    assert states == (
        ("avatar_profile_family_default", "family_safe_persona", "consent_required"),
        ("avatar_profile_operator_assist", "operator_assist_persona", "consent_confirmed"),
        ("avatar_profile_child_guarded", "child_guarded_persona", "guardian_consent_confirmed"),
    )
