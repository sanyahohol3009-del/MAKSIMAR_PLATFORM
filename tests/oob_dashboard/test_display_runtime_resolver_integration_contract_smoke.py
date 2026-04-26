from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_integration_contract import (
    build_display_runtime_resolver_integration_contract,
    resolve_fallback_display_target_id,
)


def test_display_runtime_resolver_integration_contract_builds() -> None:
    contract = build_display_runtime_resolver_integration_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_display_runtime_resolver_integration_foundation_entries() -> None:
    contract = build_display_runtime_resolver_integration_contract()
    resolver_map = {entry.panel_id: entry for entry in contract.entries}

    assert resolver_map["system_status"].display_target_id == "display_foundation_primary"
    assert resolver_map["system_status"].fallback_display_target_id == (
        "display_foundation_secondary"
    )
    assert resolver_map["logs"].display_target_id == "display_foundation_secondary"
    assert resolver_map["logs"].fallback_display_target_id == (
        "display_foundation_primary"
    )


def test_display_runtime_resolver_integration_interaction_entries() -> None:
    contract = build_display_runtime_resolver_integration_contract()
    resolver_map = {entry.panel_id: entry for entry in contract.entries}

    assert resolver_map["action_queue"].display_target_id == "display_operator_interaction"
    assert resolver_map["action_queue"].fallback_display_target_id == (
        "display_operator_interaction"
    )
    assert resolver_map["audit_timeline"].resolved_display_role == (
        "operator_interaction_display"
    )


def test_resolve_fallback_display_target_id_smoke() -> None:
    assert resolve_fallback_display_target_id("display_foundation_primary") == (
        "display_foundation_secondary"
    )
    assert resolve_fallback_display_target_id("display_foundation_secondary") == (
        "display_foundation_primary"
    )
    assert resolve_fallback_display_target_id("display_operator_interaction") == (
        "display_operator_interaction"
    )
