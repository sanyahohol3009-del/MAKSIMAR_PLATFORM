from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_MEMORY_DOMAINS = ("app_memory", "chat_memory")
_ALLOWED_MONOTONIC_POLICIES = ("non_decreasing", "strictly_forward")
_REF_PREFIXES = ("cursor://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must start with one of {_REF_PREFIXES}")
    return value


def _ensure_memory_domain(value: str) -> str:
    value = _ensure_non_empty(value, "memory_domain")
    if value not in _ALLOWED_MEMORY_DOMAINS:
        raise ValueError(f"memory_domain must be one of {_ALLOWED_MEMORY_DOMAINS}")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


@dataclass(frozen=True)
class MobileSyncCursorContract:
    cursor_id: str
    memory_domain: str
    source_device_id: str
    previous_sequence: int
    accepted_sequence: int
    previous_checkpoint_ref: str
    accepted_checkpoint_ref: str
    monotonic_policy: str
    persistence_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "cursor_id", _ensure_non_empty(self.cursor_id, "cursor_id"))
        object.__setattr__(self, "memory_domain", _ensure_memory_domain(self.memory_domain))
        object.__setattr__(self, "source_device_id", _ensure_non_empty(self.source_device_id, "source_device_id"))
        object.__setattr__(self, "previous_sequence", _ensure_non_negative_int(self.previous_sequence, "previous_sequence"))
        object.__setattr__(self, "accepted_sequence", _ensure_non_negative_int(self.accepted_sequence, "accepted_sequence"))
        object.__setattr__(self, "previous_checkpoint_ref", _ensure_ref(self.previous_checkpoint_ref, "previous_checkpoint_ref"))
        object.__setattr__(self, "accepted_checkpoint_ref", _ensure_ref(self.accepted_checkpoint_ref, "accepted_checkpoint_ref"))
        object.__setattr__(self, "monotonic_policy", _ensure_non_empty(self.monotonic_policy, "monotonic_policy"))

        if self.monotonic_policy not in _ALLOWED_MONOTONIC_POLICIES:
            raise ValueError(f"monotonic_policy must be one of {_ALLOWED_MONOTONIC_POLICIES}")
        if self.accepted_sequence < self.previous_sequence:
            raise ValueError("accepted_sequence must be greater than or equal to previous_sequence")
        if self.monotonic_policy == "strictly_forward" and self.accepted_sequence <= self.previous_sequence:
            raise ValueError("accepted_sequence must be greater than previous_sequence for strictly_forward policy")

        required_false = {
            "persistence_allowed": self.persistence_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def advance(
        cls,
        *,
        cursor_id: str,
        memory_domain: str,
        source_device_id: str,
        previous_sequence: int,
        accepted_sequence: int,
        monotonic_policy: str = "non_decreasing",
    ) -> "MobileSyncCursorContract":
        return cls(
            cursor_id=cursor_id,
            memory_domain=memory_domain,
            source_device_id=source_device_id,
            previous_sequence=previous_sequence,
            accepted_sequence=accepted_sequence,
            previous_checkpoint_ref=f"cursor://{source_device_id}/{memory_domain}/{previous_sequence}",
            accepted_checkpoint_ref=f"cursor://{source_device_id}/{memory_domain}/{accepted_sequence}",
            monotonic_policy=monotonic_policy,
            persistence_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            runtime_mutation_allowed=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "cursor_id": self.cursor_id,
            "memory_domain": self.memory_domain,
            "source_device_id": self.source_device_id,
            "previous_sequence": self.previous_sequence,
            "accepted_sequence": self.accepted_sequence,
            "previous_checkpoint_ref": self.previous_checkpoint_ref,
            "accepted_checkpoint_ref": self.accepted_checkpoint_ref,
            "monotonic_policy": self.monotonic_policy,
            "cursor_regression_allowed": False,
            "network_allowed": self.network_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
        }
