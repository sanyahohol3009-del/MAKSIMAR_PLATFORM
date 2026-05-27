import pytest

from MAKSIMAR_CORE_LIB.chat_command.server_sync_contract import ServerSyncContract


def test_server_sync_contract_smoke() -> None:
    sync = ServerSyncContract(
        sync_id="sync_001",
        source_node_id="server_main",
        target_node_id="android_device_001",
        sync_scope="message_reference",
        sync_state="declared",
        conflict_policy="owner_review",
        encryption_required=True,
        operator_approval_required=True,
        direct_sync_execution_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert sync.encryption_required is True
    assert sync.operator_approval_required is True


def test_server_sync_rejects_external_network_access() -> None:
    with pytest.raises(ValueError, match="external_network_access_allowed must be False"):
        ServerSyncContract(
            sync_id="sync_bad",
            source_node_id="server_main",
            target_node_id="ios_device_001",
            sync_scope="message_reference",
            sync_state="declared",
            conflict_policy="owner_review",
            encryption_required=True,
            operator_approval_required=True,
            direct_sync_execution_allowed=False,
            external_network_access_allowed=True,
            runtime_mutation_allowed=False,
        )
