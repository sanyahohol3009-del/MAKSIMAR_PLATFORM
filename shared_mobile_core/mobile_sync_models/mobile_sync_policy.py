from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_MEMORY_DOMAINS = ("app_memory", "chat_memory")
_POLICY_REF_PREFIXES = ("policy://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_policy_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_POLICY_REF_PREFIXES):
        raise ValueError(f"{field_name} must start with one of {_POLICY_REF_PREFIXES}")
    return value


def _ensure_domains(values: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("allowed_memory_domains must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "allowed_memory_domain") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("allowed_memory_domains must not contain duplicates")
    for value in normalized:
        if value not in _ALLOWED_MEMORY_DOMAINS:
            raise ValueError(f"allowed_memory_domains values must be one of {_ALLOWED_MEMORY_DOMAINS}")
    return normalized


@dataclass(frozen=True)
class MobileSyncPolicy:
    policy_id: str
    policy_ref: str
    allowed_memory_domains: tuple[str, ...]
    policy_boundary_required: bool
    encryption_required: bool
    retention_required: bool
    audit_required: bool
    conflict_policy_required: bool
    offline_first_required: bool
    owner_approval_required_for_replay: bool
    device_approval_required_for_replay: bool
    trusted_server_presence_required: bool
    automatic_sync_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", _ensure_non_empty(self.policy_id, "policy_id"))
        object.__setattr__(self, "policy_ref", _ensure_policy_ref(self.policy_ref, "policy_ref"))
        object.__setattr__(self, "allowed_memory_domains", _ensure_domains(self.allowed_memory_domains))

        required_true = {
            "policy_boundary_required": self.policy_boundary_required,
            "encryption_required": self.encryption_required,
            "retention_required": self.retention_required,
            "audit_required": self.audit_required,
            "conflict_policy_required": self.conflict_policy_required,
            "offline_first_required": self.offline_first_required,
            "owner_approval_required_for_replay": self.owner_approval_required_for_replay,
            "device_approval_required_for_replay": self.device_approval_required_for_replay,
            "trusted_server_presence_required": self.trusted_server_presence_required,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def strict_default(cls, *, policy_id: str) -> "MobileSyncPolicy":
        return cls(
            policy_id=policy_id,
            policy_ref=f"policy://{policy_id}",
            allowed_memory_domains=("app_memory", "chat_memory"),
            policy_boundary_required=True,
            encryption_required=True,
            retention_required=True,
            audit_required=True,
            conflict_policy_required=True,
            offline_first_required=True,
            owner_approval_required_for_replay=True,
            device_approval_required_for_replay=True,
            trusted_server_presence_required=True,
            automatic_sync_allowed=True,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    def allows_domain(self, memory_domain: str) -> bool:
        return memory_domain in self.allowed_memory_domains

    def to_read_model(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_ref": self.policy_ref,
            "allowed_memory_domains": self.allowed_memory_domains,
            "policy_boundary_required": self.policy_boundary_required,
            "automatic_sync_allowed": self.automatic_sync_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
