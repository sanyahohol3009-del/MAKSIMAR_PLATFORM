from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


_SERVER_PRESENCE_REF_PREFIXES = ("server-presence://", "ref://")
_ALLOWED_DEFERRED_REASONS = (
    "not_deferred",
    "server_absent",
    "server_untrusted",
    "automatic_sync_disabled_by_policy",
)


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_SERVER_PRESENCE_REF_PREFIXES):
        raise ValueError(f"{field_name} must start with one of {_SERVER_PRESENCE_REF_PREFIXES}")
    return value


@dataclass(frozen=True)
class ServerPresenceSyncTrigger:
    trigger_id: str
    policy: MobileSyncPolicy
    server_presence_ref: str
    server_present: bool
    trusted_server_presence: bool
    automatic_sync_enabled: bool
    deferred_reason: str
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool
    opens_runtime_connection: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "trigger_id", _ensure_non_empty(self.trigger_id, "trigger_id"))
        if not isinstance(self.policy, MobileSyncPolicy):
            raise ValueError("policy must be MobileSyncPolicy")
        object.__setattr__(self, "server_presence_ref", _ensure_ref(self.server_presence_ref, "server_presence_ref"))
        object.__setattr__(self, "deferred_reason", _ensure_non_empty(self.deferred_reason, "deferred_reason"))

        if self.deferred_reason not in _ALLOWED_DEFERRED_REASONS:
            raise ValueError(f"deferred_reason must be one of {_ALLOWED_DEFERRED_REASONS}")
        if self.automatic_sync_enabled and not self.policy.automatic_sync_allowed:
            raise ValueError("automatic_sync_enabled requires policy automatic_sync_allowed")
        if self.automatic_sync_enabled and not self.server_present:
            raise ValueError("automatic_sync_enabled requires server_present")
        if self.automatic_sync_enabled and not self.trusted_server_presence:
            raise ValueError("automatic_sync_enabled requires trusted_server_presence")
        if self.automatic_sync_enabled and self.deferred_reason != "not_deferred":
            raise ValueError("deferred_reason must be not_deferred when automatic_sync_enabled is True")
        if not self.automatic_sync_enabled and self.deferred_reason == "not_deferred":
            raise ValueError("deferred_reason must explain why automatic sync is disabled")

        required_false = {
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "opens_runtime_connection": self.opens_runtime_connection,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def evaluate(
        cls,
        *,
        trigger_id: str,
        policy: MobileSyncPolicy,
        server_presence_ref: str,
        server_present: bool,
        trusted_server_presence: bool,
    ) -> "ServerPresenceSyncTrigger":
        if not policy.automatic_sync_allowed:
            enabled = False
            reason = "automatic_sync_disabled_by_policy"
        elif not server_present:
            enabled = False
            reason = "server_absent"
        elif not trusted_server_presence:
            enabled = False
            reason = "server_untrusted"
        else:
            enabled = True
            reason = "not_deferred"

        return cls(
            trigger_id=trigger_id,
            policy=policy,
            server_presence_ref=server_presence_ref,
            server_present=server_present,
            trusted_server_presence=trusted_server_presence,
            automatic_sync_enabled=enabled,
            deferred_reason=reason,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
            opens_runtime_connection=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "trigger_id": self.trigger_id,
            "server_presence_ref": self.server_presence_ref,
            "server_present": self.server_present,
            "trusted_server_presence": self.trusted_server_presence,
            "automatic_sync_enabled": self.automatic_sync_enabled,
            "deferred_reason": self.deferred_reason,
            "network_allowed": self.network_allowed,
            "opens_runtime_connection": self.opens_runtime_connection,
            "direct_server_write_allowed": self.direct_server_write_allowed,
        }
