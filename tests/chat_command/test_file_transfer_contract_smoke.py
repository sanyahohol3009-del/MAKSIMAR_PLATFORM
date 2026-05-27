import pytest

from MAKSIMAR_CORE_LIB.chat_command.file_transfer_contract import FileTransferContract


def test_file_transfer_contract_smoke() -> None:
    transfer = FileTransferContract(
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

    assert transfer.checksum_required is True
    assert transfer.encryption_required is True


def test_file_transfer_rejects_direct_file_write() -> None:
    with pytest.raises(ValueError, match="direct_file_system_write_allowed must be False"):
        FileTransferContract(
            transfer_id="transfer_bad",
            message_id="msg_001",
            attachment_id="att_001",
            source_path_ref="local://tmp",
            storage_scope="local_cache",
            transfer_state="declared",
            size_bytes=1,
            checksum_required=True,
            encryption_required=True,
            direct_file_system_write_allowed=True,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
