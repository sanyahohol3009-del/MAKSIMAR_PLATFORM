import pytest

from ANDROID_SHELL.memory_adapter.android_memory_retention_runtime import AndroidMemoryRetentionRuntime


def test_android_memory_retention_runtime_is_policy_metadata_only() -> None:
    runtime = AndroidMemoryRetentionRuntime.default_runtime(
        retention_runtime_id="android_retention_runtime_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        android_package_name="de.maksimar.mobile",
    )

    assert runtime.purge_on_owner_request is True
    assert runtime.preserve_audit_refs is True
    assert runtime.local_only is True
    assert runtime.server_deletion_requires_sync_policy is True
    assert runtime.local_policy_evaluation_only is True
    assert runtime.real_purge_execution_allowed is False
    assert runtime.canonical_truth is False
    assert runtime.core_write_allowed is False
    assert runtime.direct_server_write_allowed is False
    assert runtime.network_allowed is False


def test_android_memory_retention_runtime_rejects_real_purge_execution() -> None:
    base = AndroidMemoryRetentionRuntime.default_runtime(
        retention_runtime_id="android_retention_runtime_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        android_package_name="de.maksimar.mobile",
    )

    with pytest.raises(ValueError, match="real_purge_execution_allowed must be False"):
        AndroidMemoryRetentionRuntime(
            retention_runtime_id="bad_retention_runtime",
            device_id=base.device_id,
            app_id=base.app_id,
            android_package_name=base.android_package_name,
            retention_policy=base.retention_policy,
            deletion_request_ref=base.deletion_request_ref,
            purge_on_logout=True,
            purge_on_owner_request=True,
            preserve_audit_refs=True,
            local_only=True,
            server_deletion_requires_sync_policy=True,
            local_policy_evaluation_only=True,
            real_purge_execution_allowed=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
        )
