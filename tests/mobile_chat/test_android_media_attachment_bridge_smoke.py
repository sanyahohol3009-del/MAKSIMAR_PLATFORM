import pytest

from ANDROID_SHELL.chat_client.media_attachment_bridge import AndroidMediaAttachmentBridgeContract


def test_android_media_attachment_bridge_smoke() -> None:
    bridge = AndroidMediaAttachmentBridgeContract(
        bridge_id="android_media_bridge_001",
        attachment_id="att_001",
        message_id="msg_001",
        media_kind="image",
        mime_type="image/png",
        preview_state="metadata_only",
        scan_required=True,
        quarantine_required=True,
        metadata_only=True,
        direct_media_render_allowed=False,
        thumbnail_generation_allowed=False,
        android_media_api_call_allowed=False,
        external_network_access_allowed=False,
        runtime_execution_allowed=False,
    )

    assert bridge.metadata_only is True
    assert bridge.direct_media_render_allowed is False
    assert bridge.thumbnail_generation_allowed is False


def test_android_media_attachment_bridge_rejects_direct_render() -> None:
    with pytest.raises(ValueError, match="direct_media_render_allowed must be False"):
        AndroidMediaAttachmentBridgeContract(
            bridge_id="android_media_bridge_bad",
            attachment_id="att_bad",
            message_id="msg_001",
            media_kind="image",
            mime_type="image/png",
            preview_state="metadata_only",
            scan_required=True,
            quarantine_required=True,
            metadata_only=True,
            direct_media_render_allowed=True,
            thumbnail_generation_allowed=False,
            android_media_api_call_allowed=False,
            external_network_access_allowed=False,
            runtime_execution_allowed=False,
        )


def test_android_media_attachment_bridge_rejects_android_media_api_call() -> None:
    with pytest.raises(ValueError, match="android_media_api_call_allowed must be False"):
        AndroidMediaAttachmentBridgeContract(
            bridge_id="android_media_bridge_api_bad",
            attachment_id="att_bad",
            message_id="msg_001",
            media_kind="video",
            mime_type="video/mp4",
            preview_state="metadata_only",
            scan_required=True,
            quarantine_required=True,
            metadata_only=True,
            direct_media_render_allowed=False,
            thumbnail_generation_allowed=False,
            android_media_api_call_allowed=True,
            external_network_access_allowed=False,
            runtime_execution_allowed=False,
        )
