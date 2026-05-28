from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_SYNC_STATUSES = (
    "ready_read_only",
    "safe_disabled",
    "degraded_read_only",
)
_ALLOWED_SERVER_PRESENCE_STATUSES = (
    "trusted_present",
    "server_absent",
    "server_untrusted",
    "not_checked",
)
_REF_PREFIXES = ("policy://", "session://", "runtime://", "sync://", "conflict://", "ref://")


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
class MobileSyncStatusReadModel:
    status_id: str
    sync_status: str
    policy_ref: str
    source_refs: tuple[str, ...]
    session_count: int
    app_sync_decision_count: int
    chat_sync_decision_count: int
    conflict_resolution_count: int
    server_presence_status: str
    automatic_sync_enabled: bool
    preview_only: bool
    read_only: bool
    sync_execution_allowed: bool
    dashboard_action_execution_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool
    mutates_runtime_state: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool
    platform_api_call_allowed: bool
    fake_success_allowed: bool
    silent_success_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "status_id", _ensure_non_empty(self.status_id, "status_id"))
        object.__setattr__(self, "sync_status", _ensure_non_empty(self.sync_status, "sync_status"))
        object.__setattr__(self, "policy_ref", _ensure_non_empty(self.policy_ref, "policy_ref"))
        object.__setattr__(self, "server_presence_status", _ensure_non_empty(self.server_presence_status, "server_presence_status"))
        object.__setattr__(self, "source_refs", _ensure_refs(self.source_refs, "source_refs"))

        if not self.policy_ref.startswith(("policy://", "ref://")):
            raise ValueError("policy_ref must start with policy:// or ref://")
        if self.sync_status not in _ALLOWED_SYNC_STATUSES:
            raise ValueError(f"sync_status must be one of {_ALLOWED_SYNC_STATUSES}")
        if self.server_presence_status not in _ALLOWED_SERVER_PRESENCE_STATUSES:
            raise ValueError(f"server_presence_status must be one of {_ALLOWED_SERVER_PRESENCE_STATUSES}")

        for field_name in (
            "session_count",
            "app_sync_decision_count",
            "chat_sync_decision_count",
            "conflict_resolution_count",
        ):
            object.__setattr__(self, field_name, _ensure_non_negative_int(getattr(self, field_name), field_name))

        required_true = {
            "preview_only": self.preview_only,
            "read_only": self.read_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "sync_execution_allowed": self.sync_execution_allowed,
            "dashboard_action_execution_allowed": self.dashboard_action_execution_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_runtime_state": self.mutates_runtime_state,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
            "platform_api_call_allowed": self.platform_api_call_allowed,
            "fake_success_allowed": self.fake_success_allowed,
            "silent_success_allowed": self.silent_success_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

        if self.automatic_sync_enabled and self.server_presence_status != "trusted_present":
            raise ValueError("automatic_sync_enabled requires trusted_present server_presence_status")

    @classmethod
    def safe_default(cls) -> "MobileSyncStatusReadModel":
        return cls(
            status_id="mobile_sync_status_default",
            sync_status="ready_read_only",
            policy_ref="policy://mobile_sync_policy_001",
            source_refs=(
                "sync://mobile_sync_envelope_contract",
                "sync://mobile_sync_cursor_contract",
                "runtime://mobile_sync_session_registry",
                "runtime://app_memory_sync_runtime",
                "runtime://chat_memory_sync_runtime",
                "conflict://mobile_sync_conflict_resolver",
            ),
            session_count=0,
            app_sync_decision_count=0,
            chat_sync_decision_count=0,
            conflict_resolution_count=0,
            server_presence_status="not_checked",
            automatic_sync_enabled=False,
            preview_only=True,
            read_only=True,
            sync_execution_allowed=False,
            dashboard_action_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_runtime_state=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
            platform_api_call_allowed=False,
            fake_success_allowed=False,
            silent_success_allowed=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "status_id": self.status_id,
            "sync_status": self.sync_status,
            "policy_ref": self.policy_ref,
            "source_refs": self.source_refs,
            "session_count": self.session_count,
            "app_sync_decision_count": self.app_sync_decision_count,
            "chat_sync_decision_count": self.chat_sync_decision_count,
            "conflict_resolution_count": self.conflict_resolution_count,
            "server_presence_status": self.server_presence_status,
            "automatic_sync_enabled": self.automatic_sync_enabled,
            "preview_only": self.preview_only,
            "read_only": self.read_only,
            "sync_execution_allowed": self.sync_execution_allowed,
            "dashboard_action_execution_allowed": self.dashboard_action_execution_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_runtime_state": self.mutates_runtime_state,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
            "platform_api_call_allowed": self.platform_api_call_allowed,
            "fake_success_allowed": self.fake_success_allowed,
            "silent_success_allowed": self.silent_success_allowed,
        }
