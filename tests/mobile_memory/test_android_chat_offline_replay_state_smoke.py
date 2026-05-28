import pytest

from ANDROID_SHELL.memory_adapter.android_chat_offline_replay_state import AndroidChatOfflineReplayState


_RECORD_REFS = ("chat-memory://android_device_001/records/message_001",)


def test_android_chat_offline_replay_state_is_policy_metadata_only() -> None:
    state = AndroidChatOfflineReplayState.default_state(
        state_id="android_chat_replay_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
        replay_record_refs=_RECORD_REFS,
    )

    assert state.offline_replay_enabled is True
    assert state.offline_replay_policy_required is True
    assert state.sync_requires_policy is True
    assert state.local_chat_memory_only is True
    assert state.openim_truth is False
    assert state.core_chat_truth is False
    assert state.canonical_truth is False
    assert state.delivery_semantics_defined is False
    assert state.network_allowed is False
    assert state.real_replay_execution_allowed is False


def test_android_chat_offline_replay_state_rejects_delivery_semantics() -> None:
    base = AndroidChatOfflineReplayState.default_state(
        state_id="android_chat_replay_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
        replay_record_refs=_RECORD_REFS,
    )

    with pytest.raises(ValueError, match="delivery_semantics_defined must be False"):
        AndroidChatOfflineReplayState(
            state_id="bad_replay",
            device_id=base.device_id,
            app_id=base.app_id,
            owner_identity_id=base.owner_identity_id,
            android_package_name=base.android_package_name,
            replay_record_refs=base.replay_record_refs,
            replay_cursor_ref=base.replay_cursor_ref,
            retention_policy=base.retention_policy,
            offline_replay_enabled=True,
            offline_replay_policy_required=True,
            sync_requires_policy=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            delivery_semantics_defined=True,
            network_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            real_replay_execution_allowed=False,
        )
