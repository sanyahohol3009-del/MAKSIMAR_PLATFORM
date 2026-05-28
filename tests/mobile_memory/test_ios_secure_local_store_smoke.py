import pytest

from IOS_SHELL.memory_adapter.ios_secure_local_store import IOSSecureLocalStore


def test_ios_secure_local_store_keeps_reference_only_boundary() -> None:
    store = IOSSecureLocalStore.default_secure_store(
        local_store_id="ios_secure_store_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        ios_bundle_id="de.maksimar.mobile",
    )

    assert store.encrypted_at_rest_required is True
    assert store.key_material_embedded is False
    assert store.plaintext_allowed is False
    assert store.local_app_memory_only is True
    assert store.shell_adapter_only is True
    assert store.canonical_truth is False
    assert store.core_write_allowed is False
    assert store.direct_server_write_allowed is False
    assert store.file_io_allowed is False
    assert store.network_allowed is False


def test_ios_secure_local_store_rejects_plaintext() -> None:
    with pytest.raises(ValueError, match="plaintext_allowed must be False"):
        IOSSecureLocalStore(
            local_store_id="bad_store",
            device_id="ios_device_001",
            app_id="maksimar_mobile",
            ios_bundle_id="de.maksimar.mobile",
            storage_scope="ios_app_sandbox",
            storage_ref="ios-secure-ref://ios_device_001/app-memory/bad",
            encrypted_at_rest_required=True,
            key_material_embedded=False,
            plaintext_allowed=True,
            local_app_memory_only=True,
            shell_adapter_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            file_io_allowed=False,
            network_allowed=False,
            supported_record_kinds=("app_state",),
        )
