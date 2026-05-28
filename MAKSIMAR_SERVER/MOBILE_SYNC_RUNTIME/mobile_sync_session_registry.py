from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


_SESSION_REF_PREFIXES = ("session://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_session_ref(value: str) -> str:
    value = _ensure_non_empty(value, "session_ref")
    if not value.startswith(_SESSION_REF_PREFIXES):
        raise ValueError(f"session_ref must start with one of {_SESSION_REF_PREFIXES}")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


@dataclass(frozen=True)
class MobileSyncSessionState:
    session_id: str
    owner_identity_id: str
    device_id: str
    app_id: str
    policy: MobileSyncPolicy
    created_at_epoch_ms: int
    session_ref: str
    read_only_state: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_connection_allowed: bool
    canonical_state_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        for field_name in ("session_id", "owner_identity_id", "device_id", "app_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.policy, MobileSyncPolicy):
            raise ValueError("policy must be MobileSyncPolicy")

        object.__setattr__(
            self,
            "created_at_epoch_ms",
            _ensure_non_negative_int(self.created_at_epoch_ms, "created_at_epoch_ms"),
        )
        object.__setattr__(self, "session_ref", _ensure_session_ref(self.session_ref))

        if self.read_only_state is not True:
            raise ValueError("read_only_state must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_connection_allowed": self.runtime_connection_allowed,
            "canonical_state_mutation_allowed": self.canonical_state_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "owner_identity_id": self.owner_identity_id,
            "device_id": self.device_id,
            "app_id": self.app_id,
            "policy_ref": self.policy.policy_ref,
            "created_at_epoch_ms": self.created_at_epoch_ms,
            "session_ref": self.session_ref,
            "read_only_state": self.read_only_state,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }


@dataclass
class MobileSyncSessionRegistry:
    registry_id: str
    _sessions: dict[str, MobileSyncSessionState] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.registry_id = _ensure_non_empty(self.registry_id, "registry_id")
        if not isinstance(self._sessions, dict):
            raise ValueError("_sessions must be a dictionary")
        if len(set(self._sessions)) != len(self._sessions):
            raise ValueError("_sessions must not contain duplicate session ids")
        for session_id, session in self._sessions.items():
            if not isinstance(session, MobileSyncSessionState):
                raise ValueError("_sessions values must be MobileSyncSessionState")
            if session.session_id != session_id:
                raise ValueError("_sessions keys must match session.session_id")

    def create_session(
        self,
        *,
        session_id: str,
        owner_identity_id: str,
        device_id: str,
        app_id: str,
        policy: MobileSyncPolicy,
        created_at_epoch_ms: int,
    ) -> MobileSyncSessionState:
        session_id = _ensure_non_empty(session_id, "session_id")
        if session_id in self._sessions:
            raise ValueError("duplicate mobile sync session id")

        session = MobileSyncSessionState(
            session_id=session_id,
            owner_identity_id=owner_identity_id,
            device_id=device_id,
            app_id=app_id,
            policy=policy,
            created_at_epoch_ms=created_at_epoch_ms,
            session_ref=f"session://{session_id}",
            read_only_state=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            canonical_state_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> MobileSyncSessionState:
        session_id = _ensure_non_empty(session_id, "session_id")
        if session_id not in self._sessions:
            raise ValueError("mobile sync session not found")
        return self._sessions[session_id]

    def list_session_read_models(self) -> tuple[dict[str, Any], ...]:
        return tuple(session.to_read_model() for session in self._sessions.values())
