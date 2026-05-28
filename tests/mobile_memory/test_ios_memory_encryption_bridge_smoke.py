import pytest

from IOS_SHELL.memory_adapter.ios_memory_encryption_bridge import IOSMemoryEncryptionBridge


def test_ios_memory_encryption_bridge_is_metadata_only() -> None:
    bridge = IOSMemoryEncryptionBridge.default_bridge(
        bridge_id="ios_encryption_bridge_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        ios_bundle_id="de.maksimar.mobile",
    )

    assert bridge.encryption_required is True
    assert bridge.at_rest_required is True
    assert bridge.in_transit_requires_sync_policy is True
    assert bridge.key_material_embedded is False
    assert bridge.plaintext_allowed is False
    assert bridge.shell_adapter_only is True
    assert bridge.canonical_truth is False
    assert bridge.core_write_allowed is False
    assert bridge.direct_server_write_allowed is False
    assert bridge.platform_api_calls_allowed is False


def test_ios_memory_encryption_bridge_rejects_platform_api_calls() -> None:
    with pytest.raises(ValueError, match="platform_api_calls_allowed must be False"):
        IOSMemoryEncryptionBridge(
            bridge_id="bad_bridge",
            device_id="ios_device_001",
            app_id="maksimar_mobile",
            ios_bundle_id="de.maksimar.mobile",
            encryption_contract=IOSMemoryEncryptionBridge.default_bridge(
                bridge_id="base_bridge",
                device_id="ios_device_001",
                app_id="maksimar_mobile",
                ios_bundle_id="de.maksimar.mobile",
            ).encryption_contract,
            ios_keychain_ref="ios-keychain://ios_device_001/app-memory/default",
            encryption_required=True,
            at_rest_required=True,
            in_transit_requires_sync_policy=True,
            key_material_embedded=False,
            plaintext_allowed=False,
            shell_adapter_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            platform_api_calls_allowed=True,
        )
