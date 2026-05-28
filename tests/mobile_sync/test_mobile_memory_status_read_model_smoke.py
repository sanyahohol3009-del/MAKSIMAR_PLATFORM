import pytest

from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_memory_status_read_model import MobileMemoryStatusReadModel


def test_mobile_memory_status_read_model_exposes_local_reference_only_memory_state() -> None:
    model = MobileMemoryStatusReadModel.safe_default()
    read_model = model.to_read_model()

    assert read_model["app_memory_local_only"] is True
    assert read_model["chat_memory_local_only"] is True
    assert read_model["app_memory_reference_only"] is True
    assert read_model["chat_memory_reference_only"] is True
    assert read_model["read_only"] is True
    assert read_model["preview_only"] is True
    assert read_model["canonical_truth"] is False
    assert read_model["global_project_memory"] is False
    assert read_model["core_write_allowed"] is False
    assert read_model["direct_server_write_allowed"] is False
    assert read_model["network_allowed"] is False
    assert read_model["socket_allowed"] is False
    assert read_model["tunnel_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["mutates_app_memory_store"] is False
    assert read_model["mutates_chat_memory_store"] is False
    assert read_model["platform_api_call_allowed"] is False
    assert read_model["dashboard_action_execution_allowed"] is False


def test_mobile_memory_status_read_model_rejects_invalid_status_and_canonical_truth() -> None:
    with pytest.raises(ValueError, match="app_memory_status must be one of"):
        MobileMemoryStatusReadModel(
            status_id="bad_memory_status",
            app_memory_status="canonical_memory_truth",
            chat_memory_status="ready_read_only",
            source_refs=("app-memory://local-app-memory-contracts",),
            app_memory_record_ref_count=0,
            chat_memory_record_ref_count=0,
            app_memory_local_only=True,
            chat_memory_local_only=True,
            app_memory_reference_only=True,
            chat_memory_reference_only=True,
            preview_only=True,
            read_only=True,
            canonical_truth=False,
            global_project_memory=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            dashboard_action_execution_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )

    with pytest.raises(ValueError, match="canonical_truth must be False"):
        MobileMemoryStatusReadModel(
            status_id="bad_canonical_truth",
            app_memory_status="ready_read_only",
            chat_memory_status="ready_read_only",
            source_refs=("app-memory://local-app-memory-contracts",),
            app_memory_record_ref_count=0,
            chat_memory_record_ref_count=0,
            app_memory_local_only=True,
            chat_memory_local_only=True,
            app_memory_reference_only=True,
            chat_memory_reference_only=True,
            preview_only=True,
            read_only=True,
            canonical_truth=True,
            global_project_memory=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            dashboard_action_execution_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )
