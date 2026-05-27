import pytest

from ANDROID_SHELL.chat_client.chat_notification_bridge import AndroidChatNotificationBridgeContract
from ANDROID_SHELL.chat_client.chat_state_bridge import AndroidChatStateBridge, AndroidChatStateSnapshot


def test_android_chat_state_bridge_smoke() -> None:
    snapshot = AndroidChatStateBridge().build_snapshot(
        bridge_id="android_state_001",
        device_id="android_device_001",
        active_room_id="room_operator_001",
        connection_state="offline",
        unread_count=2,
        pending_outbound_count=1,
    )

    assert snapshot.dashboard_visible is True
    assert snapshot.direct_server_write_allowed is False
    assert snapshot.runtime_execution_allowed is False


def test_android_chat_state_bridge_rejects_runtime_execution() -> None:
    with pytest.raises(ValueError, match="runtime_execution_allowed must be False"):
        AndroidChatStateSnapshot(
            bridge_id="android_state_bad",
            device_id="android_device_001",
            active_room_id="room_operator_001",
            connection_state="offline",
            unread_count=0,
            pending_outbound_count=0,
            dashboard_visible=True,
            direct_server_write_allowed=False,
            runtime_execution_allowed=True,
            canonical_truth_write_allowed=False,
        )


def test_android_chat_notification_bridge_rejects_sensitive_payload() -> None:
    with pytest.raises(ValueError, match="sensitive_payload_allowed must be False"):
        AndroidChatNotificationBridgeContract(
            notification_id="notif_bad",
            message_id="msg_001",
            room_id="room_operator_001",
            title_preview="New message",
            sensitive_payload_allowed=True,
            direct_open_message_allowed=False,
            external_network_access_allowed=False,
            runtime_execution_allowed=False,
        )
