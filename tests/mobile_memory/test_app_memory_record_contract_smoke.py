from __future__ import annotations

from shared_mobile_core.app_memory.app_memory_record_contract import (
    AppMemoryRecordContract,
)


def test_app_memory_record_contract_smoke() -> None:
    record = AppMemoryRecordContract.local_preference(
        record_id="app_memory_record_001",
        app_id="maksimar_mobile",
        device_id="android_device_001",
        owner_identity_id="owner_001",
        payload_ref="app-memory://preferences/theme",
        created_at="2026-05-28T20:00:00Z",
        updated_at="2026-05-28T20:00:00Z",
        retention_policy_id="retention_001",
        encryption_policy_id="encryption_001",
        audit_ref="ref://audit/app_memory_record_001",
    )

    assert record.local_app_memory_only is True
    assert record.global_project_memory is False
    assert record.canonical_truth is False
    assert record.core_write_allowed is False
    assert record.direct_server_write_allowed is False
    assert record.sync_requires_policy is True
    assert record.payload_ref == "app-memory://preferences/theme"
