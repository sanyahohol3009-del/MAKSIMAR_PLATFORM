import pytest

from MAKSIMAR_CORE_LIB.chat_command.media_attachment_contract import MediaAttachmentContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.media_attachment_runtime import (
    MediaAttachmentRuntime,
    MediaAttachmentRuntimeRecord,
)


def _contract() -> MediaAttachmentContract:
    return MediaAttachmentContract(
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


def test_media_attachment_runtime_smoke() -> None:
    runtime = MediaAttachmentRuntime()
    record = runtime.register_attachment(_contract())

    assert record.runtime_state == "inspection_required"
    assert record.scan_required is True
    assert runtime.get_record("att_001") == record


def test_media_attachment_runtime_quarantines_reference_only() -> None:
    runtime = MediaAttachmentRuntime()
    runtime.register_attachment(_contract())

    quarantined = runtime.mark_quarantined_reference("att_001")

    assert quarantined.runtime_state == "quarantined_reference"
    assert quarantined.direct_render_allowed is False


def test_media_attachment_runtime_rejects_direct_render() -> None:
    with pytest.raises(ValueError, match="direct_render_allowed must be False"):
        MediaAttachmentRuntimeRecord(
            attachment_id="att_bad",
            message_id="msg_001",
            media_kind="image",
            runtime_state="inspection_required",
            scan_required=True,
            quarantine_required=True,
            direct_render_allowed=True,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
