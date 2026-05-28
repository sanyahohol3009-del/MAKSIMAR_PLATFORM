from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_MEMORY_STATUSES = (
    "ready_read_only",
    "safe_disabled",
    "degraded_read_only",
    "not_configured",
)
_REF_PREFIXES = ("app-memory://", "chat-memory://", "policy://", "adapter://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


def _ensure_refs(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple")
    normalized = tuple(_ensure_non_empty(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    for value in normalized:
        if not value.startswith(_REF_PREFIXES):
            raise ValueError(f"{field_name} values must start with one of {_REF_PREFIXES}")
    return normalized


@dataclass(frozen=True)
class MobileMemoryStatusReadModel:
    status_id: str
    app_memory_status: str
    chat_memory_status: str
    source_refs: tuple[str, ...]
    app_memory_record_ref_count: int
    chat_memory_record_ref_count: int
    app_memory_local_only: bool
    chat_memory_local_only: bool
    app_memory_reference_only: bool
    chat_memory_reference_only: bool
    preview_only: bool
    read_only: bool
    canonical_truth: bool
    global_project_memory: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool
    platform_api_call_allowed: bool
    dashboard_action_execution_allowed: bool
    fake_success_allowed: bool
    silent_success_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "status_id", _ensure_non_empty(self.status_id, "status_id"))
        object.__setattr__(self, "app_memory_status", _ensure_non_empty(self.app_memory_status, "app_memory_status"))
        object.__setattr__(self, "chat_memory_status", _ensure_non_empty(self.chat_memory_status, "chat_memory_status"))
        object.__setattr__(self, "source_refs", _ensure_refs(self.source_refs, "source_refs"))
        object.__setattr__(
            self,
            "app_memory_record_ref_count",
            _ensure_non_negative_int(self.app_memory_record_ref_count, "app_memory_record_ref_count"),
        )
        object.__setattr__(
            self,
            "chat_memory_record_ref_count",
            _ensure_non_negative_int(self.chat_memory_record_ref_count, "chat_memory_record_ref_count"),
        )

        if self.app_memory_status not in _ALLOWED_MEMORY_STATUSES:
            raise ValueError(f"app_memory_status must be one of {_ALLOWED_MEMORY_STATUSES}")
        if self.chat_memory_status not in _ALLOWED_MEMORY_STATUSES:
            raise ValueError(f"chat_memory_status must be one of {_ALLOWED_MEMORY_STATUSES}")

        required_true = {
            "app_memory_local_only": self.app_memory_local_only,
            "chat_memory_local_only": self.chat_memory_local_only,
            "app_memory_reference_only": self.app_memory_reference_only,
            "chat_memory_reference_only": self.chat_memory_reference_only,
            "preview_only": self.preview_only,
            "read_only": self.read_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "global_project_memory": self.global_project_memory,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
            "platform_api_call_allowed": self.platform_api_call_allowed,
            "dashboard_action_execution_allowed": self.dashboard_action_execution_allowed,
            "fake_success_allowed": self.fake_success_allowed,
            "silent_success_allowed": self.silent_success_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def safe_default(cls) -> "MobileMemoryStatusReadModel":
        return cls(
            status_id="mobile_memory_status_default",
            app_memory_status="ready_read_only",
            chat_memory_status="ready_read_only",
            source_refs=(
                "app-memory://local-app-memory-contracts",
                "chat-memory://local-chat-memory-contracts",
                "adapter://android-memory-adapter",
                "adapter://ios-memory-adapter",
                "policy://mobile_sync_policy_001",
            ),
            app_memory_record_ref_count=0,
            chat_memory_record_ref_count=0,
            app_memory_local_only=True,
            chat_memory_local_only=True,
            app_memory_reference_only=True,
            chat_memory_reference_only=True,
            preview_only=True,
            read_only=True,
            canonical_truth=False,
            global_project_memory=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            dashboard_action_execution_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "status_id": self.status_id,
            "app_memory_status": self.app_memory_status,
            "chat_memory_status": self.chat_memory_status,
            "source_refs": self.source_refs,
            "app_memory_record_ref_count": self.app_memory_record_ref_count,
            "chat_memory_record_ref_count": self.chat_memory_record_ref_count,
            "app_memory_local_only": self.app_memory_local_only,
            "chat_memory_local_only": self.chat_memory_local_only,
            "app_memory_reference_only": self.app_memory_reference_only,
            "chat_memory_reference_only": self.chat_memory_reference_only,
            "preview_only": self.preview_only,
            "read_only": self.read_only,
            "canonical_truth": self.canonical_truth,
            "global_project_memory": self.global_project_memory,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
            "platform_api_call_allowed": self.platform_api_call_allowed,
            "dashboard_action_execution_allowed": self.dashboard_action_execution_allowed,
            "fake_success_allowed": self.fake_success_allowed,
            "silent_success_allowed": self.silent_success_allowed,
        }
