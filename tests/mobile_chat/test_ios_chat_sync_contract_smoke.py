import pytest

from IOS_SHELL.chat_client.chat_sync_contract import IOSChatSyncContract


def test_ios_chat_sync_contract_smoke() -> None:
    contract = IOSChatSyncContract(
        sync_binding_id="ios_sync_001",
        device_id="ios_device_001",
        server_node_id="server_main",
        sync_mode="server_available",
        message_scope="message_reference",
        encryption_required=True,
        direct_network_call_allowed=False,
        direct_server_write_allowed=False,
        background_task_start_allowed=False,
        canonical_truth_write_allowed=False,
    )

    assert contract.encryption_required is True
    assert contract.direct_network_call_allowed is False


def test_ios_chat_sync_contract_rejects_direct_network_call() -> None:
    with pytest.raises(ValueError, match="direct_network_call_allowed must be False"):
        IOSChatSyncContract(
            sync_binding_id="ios_sync_bad",
            device_id="ios_device_001",
            server_node_id="server_main",
            sync_mode="server_available",
            message_scope="message_reference",
            encryption_required=True,
            direct_network_call_allowed=True,
            direct_server_write_allowed=False,
            background_task_start_allowed=False,
            canonical_truth_write_allowed=False,
        )
