from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class JuniorModelSyncPolicy:
    policy_id: str
    default_sync_mode: str
    sync_frequency_policy_enabled: bool
    continuous_sync_allowed: bool
    background_sync_allowed: bool
    background_sync_future_metadata_only: bool
    offline_queue_allowed: bool
    offline_queue_canonical: bool
    sync_requires_policy: bool
    sync_requires_server_presence_or_floating_master: bool
    junior_sync_authority: bool
    conflict_resolution_on_server_only: bool
    server_remains_canonical_authority: bool
    model_download_allowed: bool
    local_inference_started: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", _ensure_non_empty(self.policy_id, "policy_id"))
        object.__setattr__(self, "default_sync_mode", _ensure_non_empty(self.default_sync_mode, "default_sync_mode"))
        if self.default_sync_mode != "controlled":
            raise ValueError("default_sync_mode must be controlled")
        for field_name in (
            "sync_frequency_policy_enabled",
            "background_sync_future_metadata_only",
            "offline_queue_allowed",
            "sync_requires_policy",
            "sync_requires_server_presence_or_floating_master",
            "conflict_resolution_on_server_only",
            "server_remains_canonical_authority",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "continuous_sync_allowed",
            "background_sync_allowed",
            "offline_queue_canonical",
            "junior_sync_authority",
            "model_download_allowed",
            "local_inference_started",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "default_sync_mode": self.default_sync_mode,
            "sync_frequency_policy_enabled": self.sync_frequency_policy_enabled,
            "continuous_sync_allowed": self.continuous_sync_allowed,
            "background_sync_allowed": self.background_sync_allowed,
            "background_sync_future_metadata_only": self.background_sync_future_metadata_only,
            "offline_queue_allowed": self.offline_queue_allowed,
            "offline_queue_canonical": self.offline_queue_canonical,
            "sync_requires_policy": self.sync_requires_policy,
            "sync_requires_server_presence_or_floating_master": self.sync_requires_server_presence_or_floating_master,
            "junior_sync_authority": self.junior_sync_authority,
            "conflict_resolution_on_server_only": self.conflict_resolution_on_server_only,
            "server_remains_canonical_authority": self.server_remains_canonical_authority,
            "model_download_allowed": self.model_download_allowed,
            "local_inference_started": self.local_inference_started,
        }


def build_junior_model_sync_policy() -> JuniorModelSyncPolicy:
    return JuniorModelSyncPolicy(
        policy_id="junior_model_sync_policy_v0_1",
        default_sync_mode="controlled",
        sync_frequency_policy_enabled=True,
        continuous_sync_allowed=False,
        background_sync_allowed=False,
        background_sync_future_metadata_only=True,
        offline_queue_allowed=True,
        offline_queue_canonical=False,
        sync_requires_policy=True,
        sync_requires_server_presence_or_floating_master=True,
        junior_sync_authority=False,
        conflict_resolution_on_server_only=True,
        server_remains_canonical_authority=True,
        model_download_allowed=False,
        local_inference_started=False,
    )
