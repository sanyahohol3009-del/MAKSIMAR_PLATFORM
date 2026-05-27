import pytest

from MAKSIMAR_CORE_LIB.chat_command.media_attachment_contract import MediaAttachmentContract


def test_media_attachment_contract_smoke() -> None:
    attachment = MediaAttachmentContract(
        attachment_id="att_001",
        message_id="msg_001",
        media_kind="image",
        mime_type="image/png",
        filename="status.png",
        storage_ref="quarantine://att_001",
        attachment_state="scan_required",
        scan_required=True,
        quarantine_required=True,
        direct_render_allowed=False,
        external_network_access_allowed=False,
    )

    assert attachment.scan_required is True
    assert attachment.quarantine_required is True


def test_media_attachment_rejects_direct_render() -> None:
    with pytest.raises(ValueError, match="direct_render_allowed must be False"):
        MediaAttachmentContract(
            attachment_id="att_bad",
            message_id="msg_001",
            media_kind="image",
            mime_type="image/png",
            filename="bad.png",
            storage_ref="quarantine://bad",
            attachment_state="scan_required",
            scan_required=True,
            quarantine_required=True,
            direct_render_allowed=True,
            external_network_access_allowed=False,
        )
