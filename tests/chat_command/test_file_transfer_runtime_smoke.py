import pytest

from MAKSIMAR_CORE_LIB.chat_command.file_transfer_contract import FileTransferContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.file_transfer_runtime import (
    FileTransferRuntime,
    FileTransferRuntimeRecord,
)


def _contract() -> FileTransferContract:
    return FileTransferContract(
        transfer_id="transfer_001",
        message_id="msg_001",
        attachment_id="att_001",
        source_path_ref="quarantine://att_001",
        storage_scope="quarantine",
        transfer_state="declared",
        size_bytes=128,
        checksum_required=True,
        encryption_required=True,
        direct_file_system_write_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )


def test_file_transfer_runtime_smoke() -> None:
    runtime = FileTransferRuntime()
    record = runtime.plan_transfer(_contract())

    assert record.runtime_state == "planned_reference"
    assert record.direct_file_system_write_allowed is False
    assert runtime.get_record("transfer_001") == record


def test_file_transfer_runtime_completes_reference_only() -> None:
    runtime = FileTransferRuntime()
    runtime.plan_transfer(_contract())

    completed = runtime.mark_completed_reference("transfer_001")

    assert completed.runtime_state == "completed_reference"
    assert completed.external_network_access_allowed is False


def test_file_transfer_runtime_rejects_file_system_write() -> None:
    with pytest.raises(ValueError, match="direct_file_system_write_allowed must be False"):
        FileTransferRuntimeRecord(
            transfer_id="transfer_bad",
            message_id="msg_001",
            attachment_id="att_001",
            runtime_state="planned_reference",
            checksum_required=True,
            encryption_required=True,
            direct_file_system_write_allowed=True,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
