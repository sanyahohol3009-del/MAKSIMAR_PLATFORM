import pytest

from ANDROID_SHELL.memory_adapter.android_chat_memory_export_bridge import AndroidChatMemoryExportBridge


_RECORD_REFS = ("chat-memory://android_device_001/records/message_001",)


def test_android_chat_memory_export_bridge_is_read_only_reference_bundle() -> None:
    bridge = AndroidChatMemoryExportBridge.default_bridge(
        bridge_id="android_chat_export_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
        exported_record_refs=_RECORD_REFS,
    )

    assert bridge.export_requires_policy is True
    assert bridge.export_payload_embedded is False
    assert bridge.read_only_export is True
    assert bridge.local_chat_memory_only is True
    assert bridge.openim_truth is False
    assert bridge.core_chat_truth is False
    assert bridge.canonical_truth is False
    assert bridge.network_allowed is False
    assert bridge.file_io_allowed is False
    assert bridge.core_write_allowed is False
    assert bridge.direct_server_write_allowed is False


def test_android_chat_memory_export_bridge_rejects_embedded_payload() -> None:
    with pytest.raises(ValueError, match="export_payload_embedded must be False"):
        AndroidChatMemoryExportBridge(
            bridge_id="bad_export",
            device_id="android_device_001",
            app_id="maksimar_mobile",
            owner_identity_id="owner_001",
            android_package_name="de.maksimar.mobile",
            export_request_ref="ref://bad_export/request",
            exported_record_refs=_RECORD_REFS,
            export_format="reference_bundle",
            export_requires_policy=True,
            export_payload_embedded=True,
            read_only_export=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            network_allowed=False,
            file_io_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )
