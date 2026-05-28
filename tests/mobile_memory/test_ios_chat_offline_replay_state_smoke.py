import pytest

from IOS_SHELL.memory_adapter.ios_chat_offline_replay_state import IOSChatOfflineReplayState


_RECORD_REF = "chat-memory://ios_device_001/records/chat-memory-record-001"


def test_ios_chat_offline_replay_state_is_policy_gated_metadata() -> None:
    state = IOSChatOfflineReplayState.default_state(
        replay_state_id="ios_chat_replay_state_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
        queued_record_refs=(_RECORD_REF,),
    )

    assert state.eligible_for_replay is True
    assert state.local_policy_required is True
    assert state.server_presence_required_for_upload is True
    assert state.owner_approval_required is True
    assert state.local_chat_memory_only is True
    assert state.openim_truth is False
    assert state.core_chat_truth is False
    assert state.canonical_truth is False
    assert state.core_write_allowed is False
    assert state.direct_server_write_allowed is False
    assert state.network_allowed is False
    assert state.platform_api_calls_allowed is False
    assert state.sync_runtime_allowed is False
    assert state.mutates_queue is False
    assert state.stores_message_body is False
    assert state.stores_heavy_payload is False


def test_ios_chat_offline_replay_state_rejects_sync_runtime() -> None:
    base = IOSChatOfflineReplayState.default_state(
        replay_state_id="ios_chat_replay_state_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
        queued_record_refs=(_RECORD_REF,),
    )

    with pytest.raises(ValueError, match="sync_runtime_allowed must be False"):
        IOSChatOfflineReplayState(
            replay_state_id="bad_ios_chat_replay_state",
            device_id=base.device_id,
            app_id=base.app_id,
            owner_identity_id=base.owner_identity_id,
            ios_bundle_id=base.ios_bundle_id,
            retention_policy=base.retention_policy,
            queued_record_refs=base.queued_record_refs,
            replay_cursor_ref=base.replay_cursor_ref,
            replay_policy_ref=base.replay_policy_ref,
            audit_ref=base.audit_ref,
            eligible_for_replay=True,
            local_policy_required=True,
            server_presence_required_for_upload=True,
            owner_approval_required=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=True,
            mutates_queue=False,
            stores_message_body=False,
            stores_heavy_payload=False,
        )
