from __future__ import annotations

from MAKSIMAR_CORE_LIB.real_dashboard_clients_mobile import (
    build_real_dashboard_clients_mobile_contract,
)


def test_real_dashboard_clients_mobile_contract_builds() -> None:
    """Real dashboard / clients / mobile contract should build successfully."""
    contract = build_real_dashboard_clients_mobile_contract()

    assert contract.total_entries == 3
    assert contract.dashboard_entries == 1
    assert contract.mobile_entries == 1
    assert contract.spatial_entries == 1
    assert contract.active_entries == 3


def test_real_dashboard_clients_mobile_contract_contains_expected_dashboard_entry() -> None:
    """Real dashboard / clients / mobile should expose expected dashboard entry."""
    contract = build_real_dashboard_clients_mobile_contract()
    entry = contract.entries[0]

    assert entry.real_client_entry_id == "realclient_dashboard_001"
    assert entry.client_kind == "dashboard_client"
    assert entry.linked_orchestration_entry_id == "orchestration_control_plane_001"
    assert entry.linked_node_agent_id == "nodeagent_dev_001"
    assert entry.linked_panel_id == "panel_validation_report_001"


def test_real_dashboard_clients_mobile_contract_contains_expected_mobile_entry() -> None:
    """Real dashboard / clients / mobile should expose expected mobile entry."""
    contract = build_real_dashboard_clients_mobile_contract()
    entry = contract.entries[1]

    assert entry.real_client_entry_id == "realclient_mobile_001"
    assert entry.client_kind == "mobile_client"
    assert entry.linked_orchestration_entry_id == "orchestration_mobile_entry_001"
    assert entry.linked_node_agent_id == "nodeagent_mobile_001"
    assert entry.linked_wrist_terminal_id == "wrist_terminal_core_001"


def test_real_dashboard_clients_mobile_contract_contains_expected_ar_entry() -> None:
    """Real dashboard / clients / mobile should expose expected AR entry."""
    contract = build_real_dashboard_clients_mobile_contract()
    entry = contract.entries[2]

    assert entry.real_client_entry_id == "realclient_ar_glasses_001"
    assert entry.client_kind == "ar_glasses_client"
    assert entry.linked_orchestration_entry_id == "orchestration_mobile_entry_001"
    assert entry.linked_node_agent_id == "nodeagent_mobile_001"
    assert entry.linked_ar_display_id == "ar_glasses_display_core_001"
