import pytest

from MAKSIMAR_CORE_LIB.chat_command.server_sync_contract import ServerSyncContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.server_to_server_sync_runtime import (
    ServerToServerSyncRuntime,
    ServerToServerSyncRuntimeRecord,
)


def _contract() -> ServerSyncContract:
    return ServerSyncContract(
        sync_id="sync_001",
        source_node_id="server_main",
        target_node_id="server_backup",
        sync_scope="message_reference",
        sync_state="declared",
        conflict_policy="owner_review",
        encryption_required=True,
        operator_approval_required=True,
        direct_sync_execution_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )


def test_server_to_server_sync_runtime_smoke() -> None:
    runtime = ServerToServerSyncRuntime()
    record = runtime.plan_sync(_contract())

    assert record.runtime_state == "planned_reference"
    assert record.direct_sync_execution_allowed is False
    assert runtime.get_record("sync_001") == record


def test_server_to_server_sync_runtime_completes_reference_only() -> None:
    runtime = ServerToServerSyncRuntime()
    runtime.plan_sync(_contract())

    completed = runtime.mark_completed_reference("sync_001")

    assert completed.runtime_state == "completed_reference"
    assert completed.external_network_access_allowed is False


def test_server_to_server_sync_runtime_rejects_network_access() -> None:
    with pytest.raises(ValueError, match="external_network_access_allowed must be False"):
        ServerToServerSyncRuntimeRecord(
            sync_id="sync_bad",
            source_node_id="server_main",
            target_node_id="server_backup",
            sync_scope="message_reference",
            runtime_state="planned_reference",
            encryption_required=True,
            operator_approval_required=True,
            direct_sync_execution_allowed=False,
            external_network_access_allowed=True,
            runtime_mutation_allowed=False,
        )
