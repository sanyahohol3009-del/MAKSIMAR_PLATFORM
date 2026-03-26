from __future__ import annotations

from MAKSIMAR_CORE_LIB.full_test_suite import (
    build_full_test_suite_contract,
)


def test_full_test_suite_contract_builds() -> None:
    """Full test suite contract should build successfully."""
    contract = build_full_test_suite_contract()

    assert contract.total_entries == 3
    assert contract.orchestration_domain_entries == 1
    assert contract.clients_voice_domain_entries == 1
    assert contract.ai_transport_domain_entries == 1
    assert contract.defined_entries == 3


def test_full_test_suite_contract_contains_expected_orchestration_entry() -> None:
    """Full test suite should expose expected orchestration entry."""
    contract = build_full_test_suite_contract()
    entry = contract.entries[0]

    assert entry.full_test_entry_id == "fulltest_orchestration_001"
    assert entry.test_domain == "orchestration_domain"
    assert entry.linked_orchestration_entry_id == "orchestration_heavy_execution_001"
    assert entry.linked_transport_entry_id == "transport_dev_home_001"


def test_full_test_suite_contract_contains_expected_clients_voice_entry() -> None:
    """Full test suite should expose expected clients/voice entry."""
    contract = build_full_test_suite_contract()
    entry = contract.entries[1]

    assert entry.full_test_entry_id == "fulltest_clients_voice_001"
    assert entry.test_domain == "clients_voice_domain"
    assert entry.linked_real_client_entry_id == "realclient_mobile_001"
    assert entry.linked_real_voice_entry_id == "realvoice_show_memory_001"


def test_full_test_suite_contract_contains_expected_ai_transport_entry() -> None:
    """Full test suite should expose expected AI/transport entry."""
    contract = build_full_test_suite_contract()
    entry = contract.entries[2]

    assert entry.full_test_entry_id == "fulltest_ai_transport_001"
    assert entry.test_domain == "ai_transport_domain"
    assert entry.linked_real_ai_service_entry_id == "aiservice_visual_001"
    assert entry.linked_real_voice_entry_id == "realvoice_show_monitoring_001"
