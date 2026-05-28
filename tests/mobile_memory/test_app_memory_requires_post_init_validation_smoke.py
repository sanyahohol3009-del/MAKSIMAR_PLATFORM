from __future__ import annotations

import pytest

from shared_mobile_core.app_memory.app_memory_encryption_contract import (
    AppMemoryEncryptionContract,
)
from shared_mobile_core.app_memory.app_memory_record_contract import (
    AppMemoryRecordContract,
)
from shared_mobile_core.app_memory.app_memory_retention_policy import (
    AppMemoryRetentionPolicy,
)
from shared_mobile_core.app_memory.app_memory_store_contract import (
    AppMemoryStoreContract,
)


def _valid_record_kwargs() -> dict[str, object]:
    return {
        "record_id": "app_memory_record_001",
        "app_id": "maksimar_mobile",
        "device_id": "android_device_001",
        "owner_identity_id": "owner_001",
        "memory_scope": "local_app_state",
        "memory_kind": "app_state",
        "payload_ref": "app-memory://state/home",
        "created_at": "2026-05-28T20:00:00Z",
        "updated_at": "2026-05-28T20:00:00Z",
        "schema_version": "app_memory_record.v1",
        "privacy_classification": "local_private",
        "retention_policy_id": "retention_001",
        "encryption_policy_id": "encryption_001",
        "sync_eligible": True,
        "sync_requires_policy": True,
        "audit_ref": "ref://audit/app_memory_record_001",
        "local_app_memory_only": True,
        "global_project_memory": False,
        "canonical_truth": False,
        "core_write_allowed": False,
        "direct_server_write_allowed": False,
    }


def test_app_memory_record_rejects_empty_ids() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["record_id"] = ""

    with pytest.raises(ValueError, match="record_id must be a non-empty string"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_record_rejects_global_project_memory() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["global_project_memory"] = True

    with pytest.raises(ValueError, match="global_project_memory must be False"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_record_rejects_canonical_truth() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["canonical_truth"] = True

    with pytest.raises(ValueError, match="canonical_truth must be False"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_record_rejects_core_write() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["core_write_allowed"] = True

    with pytest.raises(ValueError, match="core_write_allowed must be False"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_record_rejects_direct_server_write() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["direct_server_write_allowed"] = True

    with pytest.raises(ValueError, match="direct_server_write_allowed must be False"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_record_rejects_inline_payload_ref() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["payload_ref"] = "inline:{\"theme\":\"dark\"}"

    with pytest.raises(ValueError, match="payload_ref must be a reference"):
        AppMemoryRecordContract(**kwargs)


def test_app_memory_store_rejects_canonical_truth() -> None:
    with pytest.raises(ValueError, match="canonical_truth must be False"):
        AppMemoryStoreContract(
            store_id="store_bad",
            device_id="android_device_001",
            app_id="maksimar_mobile",
            owner_identity_id="owner_001",
            storage_scope="app_sandbox",
            encrypted_at_rest_required=True,
            retention_required=True,
            offline_first=True,
            sync_policy_required=True,
            shell_adapter_only=True,
            canonical_truth=True,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            supported_record_kinds=("app_state",),
        )


def test_app_memory_retention_rejects_invalid_age() -> None:
    with pytest.raises(ValueError, match="max_age_days must be greater than zero"):
        AppMemoryRetentionPolicy.strict_default(max_age_days=0)


def test_app_memory_encryption_rejects_embedded_key_material() -> None:
    with pytest.raises(ValueError, match="key_ref must be a reference"):
        AppMemoryEncryptionContract.default_mobile_encryption(
            key_ref="base64:secret-key-material",
        )
