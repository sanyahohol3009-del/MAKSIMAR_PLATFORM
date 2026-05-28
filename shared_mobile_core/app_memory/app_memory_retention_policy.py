from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class AppMemoryRetentionPolicy:
    """Retention policy for local mobile app memory."""

    retention_policy_id: str
    max_age_days: int
    purge_on_logout: bool
    purge_on_owner_request: bool
    preserve_audit_refs: bool
    local_only: bool
    server_deletion_requires_sync_policy: bool

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "retention_policy_id",
            _ensure_non_empty(self.retention_policy_id, "retention_policy_id"),
        )
        if not isinstance(self.max_age_days, int) or self.max_age_days <= 0:
            raise ValueError("max_age_days must be greater than zero")
        if not self.purge_on_owner_request:
            raise ValueError("purge_on_owner_request must be True")
        if not self.preserve_audit_refs:
            raise ValueError("preserve_audit_refs must be True")
        if not self.local_only:
            raise ValueError("local_only must be True")
        if not self.server_deletion_requires_sync_policy:
            raise ValueError("server_deletion_requires_sync_policy must be True")

    @classmethod
    def strict_default(
        cls,
        *,
        retention_policy_id: str = "app_memory_retention_strict_default",
        max_age_days: int = 30,
    ) -> "AppMemoryRetentionPolicy":
        return cls(
            retention_policy_id=retention_policy_id,
            max_age_days=max_age_days,
            purge_on_logout=True,
            purge_on_owner_request=True,
            preserve_audit_refs=True,
            local_only=True,
            server_deletion_requires_sync_policy=True,
        )
