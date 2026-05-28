import pytest

from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_sync_status_read_model import MobileSyncStatusReadModel


def test_mobile_sync_status_read_model_exposes_safe_read_only_state() -> None:
    model = MobileSyncStatusReadModel.safe_default()
    read_model = model.to_read_model()

    assert read_model["read_only"] is True
    assert read_model["preview_only"] is True
    assert read_model["sync_execution_allowed"] is False
    assert read_model["dashboard_action_execution_allowed"] is False
    assert read_model["core_write_allowed"] is False
    assert read_model["direct_server_write_allowed"] is False
    assert read_model["network_allowed"] is False
    assert read_model["socket_allowed"] is False
    assert read_model["tunnel_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["mutates_runtime_state"] is False
    assert read_model["mutates_app_memory_store"] is False
    assert read_model["mutates_chat_memory_store"] is False
    assert read_model["fake_success_allowed"] is False
    assert read_model["silent_success_allowed"] is False


def test_mobile_sync_status_read_model_rejects_invalid_status_and_dashboard_execution() -> None:
    with pytest.raises(ValueError, match="sync_status must be one of"):
        MobileSyncStatusReadModel(
            status_id="bad_sync_status",
            sync_status="executing_sync",
            policy_ref="policy://mobile_sync_policy_001",
            source_refs=("sync://mobile_sync_envelope_contract",),
            session_count=0,
            app_sync_decision_count=0,
            chat_sync_decision_count=0,
            conflict_resolution_count=0,
            server_presence_status="not_checked",
            automatic_sync_enabled=False,
            preview_only=True,
            read_only=True,
            sync_execution_allowed=False,
            dashboard_action_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_runtime_state=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )

    with pytest.raises(ValueError, match="dashboard_action_execution_allowed must be False"):
        MobileSyncStatusReadModel(
            status_id="bad_dashboard_action",
            sync_status="ready_read_only",
            policy_ref="policy://mobile_sync_policy_001",
            source_refs=("sync://mobile_sync_envelope_contract",),
            session_count=0,
            app_sync_decision_count=0,
            chat_sync_decision_count=0,
            conflict_resolution_count=0,
            server_presence_status="not_checked",
            automatic_sync_enabled=False,
            preview_only=True,
            read_only=True,
            sync_execution_allowed=False,
            dashboard_action_execution_allowed=True,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_runtime_state=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )


def test_mobile_sync_status_read_model_rejects_auto_sync_without_trusted_server() -> None:
    with pytest.raises(ValueError, match="automatic_sync_enabled requires trusted_present"):
        MobileSyncStatusReadModel(
            status_id="bad_auto_sync",
            sync_status="ready_read_only",
            policy_ref="policy://mobile_sync_policy_001",
            source_refs=("sync://mobile_sync_envelope_contract",),
            session_count=0,
            app_sync_decision_count=0,
            chat_sync_decision_count=0,
            conflict_resolution_count=0,
            server_presence_status="server_absent",
            automatic_sync_enabled=True,
            preview_only=True,
            read_only=True,
            sync_execution_allowed=False,
            dashboard_action_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_runtime_state=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )
