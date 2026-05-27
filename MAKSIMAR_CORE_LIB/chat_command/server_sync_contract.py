from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SYNC_SCOPES = ("chat_metadata", "message_reference", "attachment_reference", "audit_reference")
_ALLOWED_SYNC_STATES = ("declared", "queued", "blocked", "completed_reference")
_ALLOWED_CONFLICT_POLICIES = ("manual_review", "server_precedence", "owner_review")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class ServerSyncContract:
    """Canonical server sync contract.

    Contract only. It declares sync requirements but does not run replication,
    open network connections, or write server/mobile state.
    """

    sync_id: str
    source_node_id: str
    target_node_id: str
    sync_scope: str
    sync_state: str
    conflict_policy: str
    encryption_required: bool
    operator_approval_required: bool
    direct_sync_execution_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "sync_id", _ensure_non_empty(self.sync_id, "sync_id"))
        object.__setattr__(self, "source_node_id", _ensure_non_empty(self.source_node_id, "source_node_id"))
        object.__setattr__(self, "target_node_id", _ensure_non_empty(self.target_node_id, "target_node_id"))
        object.__setattr__(self, "sync_scope", _ensure_allowed(self.sync_scope, "sync_scope", _ALLOWED_SYNC_SCOPES))
        object.__setattr__(self, "sync_state", _ensure_allowed(self.sync_state, "sync_state", _ALLOWED_SYNC_STATES))
        object.__setattr__(self, "conflict_policy", _ensure_allowed(self.conflict_policy, "conflict_policy", _ALLOWED_CONFLICT_POLICIES))

        if self.source_node_id == self.target_node_id:
            raise ValueError("source_node_id and target_node_id must differ")
        if not self.encryption_required:
            raise ValueError("encryption_required must be True")
        if not self.operator_approval_required:
            raise ValueError("operator_approval_required must be True")
        if self.direct_sync_execution_allowed:
            raise ValueError("direct_sync_execution_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
