from __future__ import annotations

from shared_mobile_core.app_memory.app_memory_retention_policy import (
    AppMemoryRetentionPolicy,
)


def test_app_memory_retention_policy_smoke() -> None:
    policy = AppMemoryRetentionPolicy.strict_default(
        retention_policy_id="retention_001",
        max_age_days=30,
    )

    assert policy.max_age_days > 0
    assert policy.purge_on_logout is True
    assert policy.purge_on_owner_request is True
    assert policy.preserve_audit_refs is True
    assert policy.local_only is True
    assert policy.server_deletion_requires_sync_policy is True
