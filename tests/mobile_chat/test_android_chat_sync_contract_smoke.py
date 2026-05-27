import pytest

from ANDROID_SHELL.chat_client.chat_sync_contract import AndroidChatSyncContract


def test_android_chat_sync_contract_smoke() -> None:
    contract = AndroidChatSyncContract(
        sync_binding_id="android_sync_001",
        device_id="android_device_001",
        server_node_id="server_main",
        sync_mode="server_available",
        message_scope="message_reference",
        encryption_required=True,
        direct_network_call_allowed=False,
        direct_server_write_allowed=False,
        background_service_start_allowed=False,
        canonical_truth_write_allowed=False,
    )

    assert contract.encryption_required is True
    assert contract.direct_network_call_allowed is False


def test_android_chat_sync_contract_rejects_direct_network_call() -> None:
    with pytest.raises(ValueError, match="direct_network_call_allowed must be False"):
        AndroidChatSyncContract(
            sync_binding_id="android_sync_bad",
            device_id="android_device_001",
            server_node_id="server_main",
            sync_mode="server_available",
            message_scope="message_reference",
            encryption_required=True,
            direct_network_call_allowed=True,
            direct_server_write_allowed=False,
            background_service_start_allowed=False,
            canonical_truth_write_allowed=False,
        )
