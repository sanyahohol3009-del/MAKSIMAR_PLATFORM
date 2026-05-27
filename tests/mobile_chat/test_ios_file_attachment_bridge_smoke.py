import pytest

from IOS_SHELL.chat_client.file_attachment_bridge import IOSFileAttachmentBridgeContract


def test_ios_file_attachment_bridge_smoke() -> None:
    bridge = IOSFileAttachmentBridgeContract(
        bridge_id="ios_file_bridge_001",
        attachment_id="att_001",
        message_id="msg_001",
        filename="report.pdf",
        storage_scope="quarantine_reference",
        attachment_state="scan_required",
        size_bytes=1024,
        checksum_required=True,
        encryption_required=True,
        scan_required=True,
        direct_file_read_allowed=False,
        direct_file_write_allowed=False,
        external_network_access_allowed=False,
        ios_file_api_call_allowed=False,
    )

    assert bridge.checksum_required is True
    assert bridge.encryption_required is True
    assert bridge.direct_file_read_allowed is False
    assert bridge.ios_file_api_call_allowed is False


def test_ios_file_attachment_bridge_rejects_direct_file_read() -> None:
    with pytest.raises(ValueError, match="direct_file_read_allowed must be False"):
        IOSFileAttachmentBridgeContract(
            bridge_id="ios_file_bridge_bad",
            attachment_id="att_bad",
            message_id="msg_001",
            filename="bad.pdf",
            storage_scope="ios_private_reference",
            attachment_state="declared",
            size_bytes=1,
            checksum_required=True,
            encryption_required=True,
            scan_required=True,
            direct_file_read_allowed=True,
            direct_file_write_allowed=False,
            external_network_access_allowed=False,
            ios_file_api_call_allowed=False,
        )


def test_ios_file_attachment_bridge_rejects_file_api_call() -> None:
    with pytest.raises(ValueError, match="ios_file_api_call_allowed must be False"):
        IOSFileAttachmentBridgeContract(
            bridge_id="ios_file_bridge_api_bad",
            attachment_id="att_bad",
            message_id="msg_001",
            filename="bad.pdf",
            storage_scope="ios_private_reference",
            attachment_state="declared",
            size_bytes=1,
            checksum_required=True,
            encryption_required=True,
            scan_required=True,
            direct_file_read_allowed=False,
            direct_file_write_allowed=False,
            external_network_access_allowed=False,
            ios_file_api_call_allowed=True,
        )
