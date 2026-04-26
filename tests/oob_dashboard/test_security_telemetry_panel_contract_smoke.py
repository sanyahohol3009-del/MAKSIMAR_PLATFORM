from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.security_telemetry_panel_contract import (
    build_security_telemetry_panel_contract,
)


def test_security_telemetry_panel_contract_builds() -> None:
    contract = build_security_telemetry_panel_contract()

    assert contract.panel_id == "panel_security_telemetry"
    assert contract.total_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.operator_visible is True


def test_security_telemetry_panel_contract_contains_expected_entries() -> None:
    contract = build_security_telemetry_panel_contract()

    states = tuple(
        (entry.telemetry_id, entry.telemetry_scope, entry.security_state)
        for entry in contract.entries
    )

    assert states == (
        ("security_telemetry_guard_chain", "guard_chain", "stable"),
        ("security_telemetry_audit_path", "audit_path", "visible_and_intact"),
        ("security_telemetry_consent_boundary", "consent_boundary", "enforced"),
    )
