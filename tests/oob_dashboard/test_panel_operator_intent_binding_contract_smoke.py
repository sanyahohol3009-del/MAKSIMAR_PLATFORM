from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_operator_intent_binding_contract import (
    build_panel_operator_intent_binding_contract,
)


def test_panel_operator_intent_binding_contract_builds() -> None:
    """Panel operator intent binding contract should build successfully."""
    contract = build_panel_operator_intent_binding_contract()

    assert contract.contract_id == "panel_operator_intent_binding_contract_001"
    assert contract.total_entries == 7
    assert contract.structurally_valid_entries == 7
    assert contract.interactive_entries == 4
    assert contract.approval_bound_entries == 1
    assert contract.read_only_fallback_entries == 4


def test_panel_operator_intent_binding_contract_marks_registered_structures() -> None:
    """Panel operator intent binding contract should mark structures as registered."""
    contract = build_panel_operator_intent_binding_contract()

    for entry in contract.entries:
        assert entry.panel_registered is True
        assert entry.workspace_registered is True
        assert entry.display_target_registered is True
        assert entry.structurally_valid is True


def test_panel_operator_intent_binding_contract_contains_expected_foundation_bindings() -> None:
    """Panel operator intent binding contract should preserve expected foundation bindings."""
    contract = build_panel_operator_intent_binding_contract()
    entry_map = {entry.panel_id: entry for entry in contract.entries}

    consistency_entry = entry_map["panel_consistency"]
    snapshot_entry = entry_map["panel_snapshot"]
    incident_entry = entry_map["panel_incident"]

    assert consistency_entry.workspace_id == "workspace_foundation_monitoring"
    assert consistency_entry.display_target_id == "display_secondary_diagnostics"
    assert consistency_entry.allowed_intent_kinds == ("view_request",)
    assert consistency_entry.interactive is False

    assert snapshot_entry.allowed_intent_kinds == ("view_request",)
    assert incident_entry.allowed_intent_kinds == ("view_request",)


def test_panel_operator_intent_binding_contract_contains_expected_operator_bindings() -> None:
    """Panel operator intent binding contract should preserve expected operator bindings."""
    contract = build_panel_operator_intent_binding_contract()
    entry_map = {entry.panel_id: entry for entry in contract.entries}

    chat_entry = entry_map["panel_chat"]
    settings_entry = entry_map["panel_settings"]
    gesture_entry = entry_map["panel_gesture_control"]

    assert chat_entry.workspace_id == "workspace_operator_main"
    assert chat_entry.display_target_id == "display_primary_operator"
    assert chat_entry.allowed_intent_kinds == (
        "view_request",
        "navigation_request",
        "approval_request",
    )
    assert chat_entry.interactive is True
    assert chat_entry.read_only_fallback is True

    assert settings_entry.allowed_intent_kinds == (
        "view_request",
        "navigation_request",
    )
    assert settings_entry.interactive is True

    assert gesture_entry.allowed_intent_kinds == (
        "view_request",
        "control_request",
        "approval_request",
    )
    assert gesture_entry.requires_explicit_approval is True
    assert gesture_entry.interactive is True
    assert gesture_entry.read_only_fallback is True


def test_panel_operator_intent_binding_contract_preserves_non_direct_execution_semantics() -> None:
    """Panel operator intent binding contract should preserve non-direct execution semantics."""
    contract = build_panel_operator_intent_binding_contract()

    for entry in contract.entries:
        assert "system_action_request" not in entry.allowed_intent_kinds

    gesture_entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_gesture_control"
    )
    assert gesture_entry.requires_explicit_approval is True
    assert gesture_entry.structurally_valid is True


def test_panel_operator_intent_binding_contract_keeps_diagnostics_panel_controlled() -> None:
    """Diagnostics panel should remain controlled and fallback-safe."""
    contract = build_panel_operator_intent_binding_contract()
    entry_map = {entry.panel_id: entry for entry in contract.entries}

    diagnostics_entry = entry_map["panel_diagnostics"]

    assert diagnostics_entry.workspace_id == "workspace_expansion_observability"
    assert diagnostics_entry.display_target_id == "display_tertiary_expansion"
    assert diagnostics_entry.allowed_intent_kinds == (
        "view_request",
        "navigation_request",
    )
    assert diagnostics_entry.interactive is True
    assert diagnostics_entry.read_only_fallback is True
