from __future__ import annotations

from MAKSIMAR_CORE_LIB.product_hardening_onboarding_packaging import (
    build_product_hardening_onboarding_packaging_contract,
)


def test_product_hardening_onboarding_packaging_contract_builds() -> None:
    """Product hardening / onboarding / packaging contract should build successfully."""
    contract = build_product_hardening_onboarding_packaging_contract()

    assert contract.total_entries == 3
    assert contract.dashboard_surface_entries == 1
    assert contract.mobile_voice_entries == 1
    assert contract.visual_ai_entries == 1
    assert contract.defined_entries == 3


def test_product_hardening_onboarding_packaging_contract_contains_expected_dashboard_entry() -> None:
    """Product package contract should expose expected dashboard entry."""
    contract = build_product_hardening_onboarding_packaging_contract()
    entry = contract.entries[0]

    assert entry.product_entry_id == "product_core_dashboard_001"
    assert entry.product_surface == "dashboard_surface"
    assert entry.linked_ops_entry_id == "ops_dev_control_001"
    assert entry.packaging_mode == "control_ready_package"


def test_product_hardening_onboarding_packaging_contract_contains_expected_mobile_entry() -> None:
    """Product package contract should expose expected mobile entry."""
    contract = build_product_hardening_onboarding_packaging_contract()
    entry = contract.entries[1]

    assert entry.product_entry_id == "product_mobile_voice_001"
    assert entry.product_surface == "mobile_voice_surface"
    assert entry.linked_ops_entry_id == "ops_mobile_proxy_001"
    assert entry.packaging_mode == "mobile_ready_package"


def test_product_hardening_onboarding_packaging_contract_contains_expected_visual_entry() -> None:
    """Product package contract should expose expected visual entry."""
    contract = build_product_hardening_onboarding_packaging_contract()
    entry = contract.entries[2]

    assert entry.product_entry_id == "product_visual_ai_001"
    assert entry.product_surface == "visual_ai_surface"
    assert entry.linked_ops_entry_id == "ops_home_execution_001"
    assert entry.packaging_mode == "visual_ready_package"
