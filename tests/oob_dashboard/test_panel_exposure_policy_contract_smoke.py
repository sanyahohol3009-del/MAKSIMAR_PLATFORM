from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)


def test_panel_exposure_policy_contract_builds() -> None:
    """Panel exposure policy contract should build successfully."""
    contract = build_panel_exposure_policy_contract()

    assert len(contract.entries) == 8


def test_panel_exposure_policy_foundation_entries() -> None:
    """Foundation panels should remain visible in both dashboards."""
    contract = build_panel_exposure_policy_contract()
    exposure_map = {entry.panel_id: entry for entry in contract.entries}

    assert exposure_map["system_status"].visible_in_oob_dashboard is True
    assert exposure_map["system_status"].visible_in_main_dashboard is True

    assert exposure_map["guard_chain"].visible_in_oob_dashboard is True
    assert exposure_map["guard_chain"].visible_in_main_dashboard is True

    assert exposure_map["incidents"].visible_in_oob_dashboard is True
    assert exposure_map["incidents"].visible_in_main_dashboard is True


def test_panel_exposure_policy_interaction_entries() -> None:
    """Interaction panels should remain visible through operator policy path."""
    contract = build_panel_exposure_policy_contract()
    exposure_map = {entry.panel_id: entry for entry in contract.entries}

    assert exposure_map["action_queue"].visibility_policy == "policy_visible"
    assert exposure_map["approval_queue"].visibility_policy == "policy_visible"
    assert exposure_map["audit_timeline"].visibility_policy == "policy_visible"


def test_panel_exposure_policy_descriptions_are_present() -> None:
    """Exposure policy entries should expose readable descriptions."""
    contract = build_panel_exposure_policy_contract()

    for entry in contract.entries:
        assert entry.description
        assert entry.exposure_level
        assert entry.visibility_policy
