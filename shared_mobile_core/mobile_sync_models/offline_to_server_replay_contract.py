from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.mobile_sync_models.mobile_sync_cursor_contract import MobileSyncCursorContract
from shared_mobile_core.mobile_sync_models.mobile_sync_envelope_contract import MobileSyncEnvelopeContract
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


_REF_PREFIXES = ("replay://", "ref://")
_AUDIT_REF_PREFIXES = ("audit://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str, allowed_prefixes: tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(allowed_prefixes):
        raise ValueError(f"{field_name} must start with one of {allowed_prefixes}")
    return value


def _ensure_record_refs(values: tuple[str, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("replay_record_refs must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "replay_record_ref") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("replay_record_refs must not contain duplicates")
    for value in normalized:
        if not value.startswith(("app-memory://", "chat-memory://")):
            raise ValueError("replay_record_refs values must be app_memory or chat_memory references")
    return normalized


@dataclass(frozen=True)
class OfflineToServerReplayContract:
    replay_id: str
    policy: MobileSyncPolicy
    envelope: MobileSyncEnvelopeContract
    cursor: MobileSyncCursorContract
    replay_record_refs: tuple[str, ...]
    replay_intent_ref: str
    audit_ref: str
    sync_policy_required: bool
    owner_approval_granted: bool
    device_approval_granted: bool
    trusted_server_presence: bool
    replay_ready: bool
    replay_execution_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "replay_id", _ensure_non_empty(self.replay_id, "replay_id"))

        if not isinstance(self.policy, MobileSyncPolicy):
            raise ValueError("policy must be MobileSyncPolicy")
        if not isinstance(self.envelope, MobileSyncEnvelopeContract):
            raise ValueError("envelope must be MobileSyncEnvelopeContract")
        if not isinstance(self.cursor, MobileSyncCursorContract):
            raise ValueError("cursor must be MobileSyncCursorContract")

        object.__setattr__(self, "replay_record_refs", _ensure_record_refs(self.replay_record_refs))
        object.__setattr__(self, "replay_intent_ref", _ensure_ref(self.replay_intent_ref, "replay_intent_ref", _REF_PREFIXES))
        object.__setattr__(self, "audit_ref", _ensure_ref(self.audit_ref, "audit_ref", _AUDIT_REF_PREFIXES))

        if not self.policy.allows_domain(self.envelope.memory_domain):
            raise ValueError("policy must allow envelope memory_domain")
        if self.cursor.memory_domain != self.envelope.memory_domain:
            raise ValueError("cursor memory_domain must match envelope memory_domain")
        if tuple(self.envelope.record_refs) != tuple(self.replay_record_refs):
            raise ValueError("replay_record_refs must match envelope record_refs")

        if self.sync_policy_required is not True:
            raise ValueError("sync_policy_required must be True")

        if self.replay_ready:
            if self.owner_approval_granted is not True:
                raise ValueError("replay_ready requires owner_approval_granted")
            if self.device_approval_granted is not True:
                raise ValueError("replay_ready requires device_approval_granted")
            if self.trusted_server_presence is not True:
                raise ValueError("replay_ready requires trusted_server_presence")
            if self.policy.policy_boundary_required is not True:
                raise ValueError("replay_ready requires policy boundary")
            if self.policy.owner_approval_required_for_replay is not True:
                raise ValueError("policy must require owner replay approval")
            if self.policy.device_approval_required_for_replay is not True:
                raise ValueError("policy must require device replay approval")

        required_false = {
            "replay_execution_allowed": self.replay_execution_allowed,
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
    def approved_replay(
        cls,
        *,
        replay_id: str,
        policy: MobileSyncPolicy,
        envelope: MobileSyncEnvelopeContract,
        cursor: MobileSyncCursorContract,
    ) -> "OfflineToServerReplayContract":
        return cls(
            replay_id=replay_id,
            policy=policy,
            envelope=envelope,
            cursor=cursor,
            replay_record_refs=envelope.record_refs,
            replay_intent_ref=f"replay://{replay_id}",
            audit_ref=f"audit://{replay_id}",
            sync_policy_required=True,
            owner_approval_granted=True,
            device_approval_granted=True,
            trusted_server_presence=True,
            replay_ready=True,
            replay_execution_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "replay_id": self.replay_id,
            "memory_domain": self.envelope.memory_domain,
            "replay_record_refs": self.replay_record_refs,
            "replay_ready": self.replay_ready,
            "sync_policy_required": self.sync_policy_required,
            "owner_approval_granted": self.owner_approval_granted,
            "device_approval_granted": self.device_approval_granted,
            "trusted_server_presence": self.trusted_server_presence,
            "replay_execution_allowed": self.replay_execution_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
