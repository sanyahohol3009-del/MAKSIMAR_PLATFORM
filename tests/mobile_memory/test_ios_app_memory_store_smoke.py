from IOS_SHELL.memory_adapter.ios_app_memory_store import IOSAppMemoryStoreAdapter


def test_ios_app_memory_store_is_shell_adapter_only() -> None:
    adapter = IOSAppMemoryStoreAdapter.default_adapter(
        adapter_id="ios_app_memory_adapter_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
    )

    assert adapter.shell_adapter_only is True
    assert adapter.local_app_memory_only is True
    assert adapter.canonical_truth is False
    assert adapter.core_write_allowed is False
    assert adapter.direct_server_write_allowed is False
    assert adapter.network_allowed is False
    assert adapter.platform_api_calls_allowed is False
    assert adapter.sync_runtime_allowed is False
    assert adapter.store_contract.canonical_truth is False
