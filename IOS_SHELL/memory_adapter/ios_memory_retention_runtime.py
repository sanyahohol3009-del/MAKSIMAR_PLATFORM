from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.app_memory import AppMemoryRetentionPolicy


_REF_PREFIXES = ("ref://", "ios-local://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a reference")
    return value


@dataclass(frozen=True)
class IOSMemoryRetentionRuntime:
    retention_runtime_id: str
    device_id: str
    app_id: str
    ios_bundle_id: str
    retention_policy: AppMemoryRetentionPolicy
    deletion_request_ref: str
    purge_on_logout: bool
    purge_on_owner_request: bool
    preserve_audit_refs: bool
    local_only: bool
    server_deletion_requires_sync_policy: bool
    local_policy_evaluation_only: bool
    real_purge_execution_allowed: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("retention_runtime_id", "device_id", "app_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.retention_policy, AppMemoryRetentionPolicy):
            raise ValueError("retention_policy must be AppMemoryRetentionPolicy")
        object.__setattr__(self, "deletion_request_ref", _ensure_ref(self.deletion_request_ref, "deletion_request_ref"))

        required_true = {
            "purge_on_owner_request": self.purge_on_owner_request,
            "preserve_audit_refs": self.preserve_audit_refs,
            "local_only": self.local_only,
            "server_deletion_requires_sync_policy": self.server_deletion_requires_sync_policy,
            "local_policy_evaluation_only": self.local_policy_evaluation_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "real_purge_execution_allowed": self.real_purge_execution_allowed,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

        if self.retention_policy.local_only is not True:
            raise ValueError("retention_policy local_only must be True")
        if self.retention_policy.server_deletion_requires_sync_policy is not True:
            raise ValueError("retention_policy server deletion must require sync policy")

    @classmethod
    def default_runtime(
        cls,
        *,
        retention_runtime_id: str,
        device_id: str,
        app_id: str,
        ios_bundle_id: str,
    ) -> "IOSMemoryRetentionRuntime":
        retention_policy = AppMemoryRetentionPolicy.strict_default(
            retention_policy_id=f"{retention_runtime_id}_policy",
            max_age_days=30,
        )
        return cls(
            retention_runtime_id=retention_runtime_id,
            device_id=device_id,
            app_id=app_id,
            ios_bundle_id=ios_bundle_id,
            retention_policy=retention_policy,
            deletion_request_ref=f"ref://{retention_runtime_id}/owner-deletion-request",
            purge_on_logout=True,
            purge_on_owner_request=True,
            preserve_audit_refs=True,
            local_only=True,
            server_deletion_requires_sync_policy=True,
            local_policy_evaluation_only=True,
            real_purge_execution_allowed=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
        )
