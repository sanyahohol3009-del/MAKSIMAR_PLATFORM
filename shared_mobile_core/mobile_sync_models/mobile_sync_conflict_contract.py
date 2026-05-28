from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any


_ALLOWED_MEMORY_DOMAINS = ("app_memory", "chat_memory")
_ALLOWED_DECISIONS = (
    "keep_local_reference",
    "keep_server_reference",
    "manual_review_required",
)
_APP_MEMORY_REF_PREFIX = "app-memory://"
_CHAT_MEMORY_REF_PREFIX = "chat-memory://"
_POLICY_REF_PREFIXES = ("policy://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_memory_domain(value: str) -> str:
    value = _ensure_non_empty(value, "memory_domain")
    if value not in _ALLOWED_MEMORY_DOMAINS:
        raise ValueError(f"memory_domain must be one of {_ALLOWED_MEMORY_DOMAINS}")
    return value


def _required_record_prefix(memory_domain: str) -> str:
    return _APP_MEMORY_REF_PREFIX if memory_domain == "app_memory" else _CHAT_MEMORY_REF_PREFIX


def _ensure_record_ref(value: str, field_name: str, memory_domain: str) -> str:
    value = _ensure_non_empty(value, field_name)
    required_prefix = _required_record_prefix(memory_domain)
    if not value.startswith(required_prefix):
        raise ValueError(f"{field_name} must start with {required_prefix}")
    return value


def _ensure_policy_ref(value: str) -> str:
    value = _ensure_non_empty(value, "conflict_policy_ref")
    if not value.startswith(_POLICY_REF_PREFIXES):
        raise ValueError(f"conflict_policy_ref must start with one of {_POLICY_REF_PREFIXES}")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


def deterministic_conflict_decision(
    *,
    local_sequence: int,
    server_sequence: int,
    local_updated_at_epoch_ms: int,
    server_updated_at_epoch_ms: int,
) -> tuple[str, str]:
    if local_sequence > server_sequence:
        return "keep_local_reference", "local_sequence_is_newer"
    if server_sequence > local_sequence:
        return "keep_server_reference", "server_sequence_is_newer"
    if local_updated_at_epoch_ms > server_updated_at_epoch_ms:
        return "keep_local_reference", "local_timestamp_is_newer"
    if server_updated_at_epoch_ms > local_updated_at_epoch_ms:
        return "keep_server_reference", "server_timestamp_is_newer"
    return "manual_review_required", "equal_sequences_and_timestamps"


@dataclass(frozen=True)
class MobileSyncConflictContract:
    conflict_id: str
    memory_domain: str
    local_record_ref: str
    server_record_ref: str
    local_sequence: int
    server_sequence: int
    local_updated_at_epoch_ms: int
    server_updated_at_epoch_ms: int
    conflict_policy_ref: str
    decision: str
    decision_reason: str
    deterministic_evidence_hash: str
    deterministic_decision_required: bool
    mutates_records: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "conflict_id", _ensure_non_empty(self.conflict_id, "conflict_id"))
        object.__setattr__(self, "memory_domain", _ensure_memory_domain(self.memory_domain))
        object.__setattr__(self, "local_record_ref", _ensure_record_ref(self.local_record_ref, "local_record_ref", self.memory_domain))
        object.__setattr__(self, "server_record_ref", _ensure_record_ref(self.server_record_ref, "server_record_ref", self.memory_domain))
        object.__setattr__(self, "local_sequence", _ensure_non_negative_int(self.local_sequence, "local_sequence"))
        object.__setattr__(self, "server_sequence", _ensure_non_negative_int(self.server_sequence, "server_sequence"))
        object.__setattr__(
            self,
            "local_updated_at_epoch_ms",
            _ensure_non_negative_int(self.local_updated_at_epoch_ms, "local_updated_at_epoch_ms"),
        )
        object.__setattr__(
            self,
            "server_updated_at_epoch_ms",
            _ensure_non_negative_int(self.server_updated_at_epoch_ms, "server_updated_at_epoch_ms"),
        )
        object.__setattr__(self, "conflict_policy_ref", _ensure_policy_ref(self.conflict_policy_ref))

        if self.decision not in _ALLOWED_DECISIONS:
            raise ValueError(f"decision must be one of {_ALLOWED_DECISIONS}")

        expected_decision, expected_reason = deterministic_conflict_decision(
            local_sequence=self.local_sequence,
            server_sequence=self.server_sequence,
            local_updated_at_epoch_ms=self.local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=self.server_updated_at_epoch_ms,
        )
        if self.decision != expected_decision:
            raise ValueError("decision must match deterministic conflict decision")
        if self.decision_reason != expected_reason:
            raise ValueError("decision_reason must match deterministic conflict reason")

        expected_hash = self._build_evidence_hash()
        if self.deterministic_evidence_hash != expected_hash:
            raise ValueError("deterministic_evidence_hash must match conflict evidence")

        if self.deterministic_decision_required is not True:
            raise ValueError("deterministic_decision_required must be True")

        required_false = {
            "mutates_records": self.mutates_records,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    def _build_evidence_hash(self) -> str:
        material = "|".join(
            (
                self.memory_domain,
                self.local_record_ref,
                self.server_record_ref,
                str(self.local_sequence),
                str(self.server_sequence),
                str(self.local_updated_at_epoch_ms),
                str(self.server_updated_at_epoch_ms),
                self.conflict_policy_ref,
                self.decision,
                self.decision_reason,
            )
        )
        return sha256(material.encode("utf-8")).hexdigest()

    @classmethod
    def decide(
        cls,
        *,
        conflict_id: str,
        memory_domain: str,
        local_record_ref: str,
        server_record_ref: str,
        local_sequence: int,
        server_sequence: int,
        local_updated_at_epoch_ms: int,
        server_updated_at_epoch_ms: int,
        conflict_policy_ref: str,
    ) -> "MobileSyncConflictContract":
        decision, reason = deterministic_conflict_decision(
            local_sequence=local_sequence,
            server_sequence=server_sequence,
            local_updated_at_epoch_ms=local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=server_updated_at_epoch_ms,
        )
        material = "|".join(
            (
                memory_domain,
                local_record_ref,
                server_record_ref,
                str(local_sequence),
                str(server_sequence),
                str(local_updated_at_epoch_ms),
                str(server_updated_at_epoch_ms),
                conflict_policy_ref,
                decision,
                reason,
            )
        )
        evidence_hash = sha256(material.encode("utf-8")).hexdigest()
        return cls(
            conflict_id=conflict_id,
            memory_domain=memory_domain,
            local_record_ref=local_record_ref,
            server_record_ref=server_record_ref,
            local_sequence=local_sequence,
            server_sequence=server_sequence,
            local_updated_at_epoch_ms=local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=server_updated_at_epoch_ms,
            conflict_policy_ref=conflict_policy_ref,
            decision=decision,
            decision_reason=reason,
            deterministic_evidence_hash=evidence_hash,
            deterministic_decision_required=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_mutation_allowed=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "memory_domain": self.memory_domain,
            "decision": self.decision,
            "decision_reason": self.decision_reason,
            "deterministic_evidence_hash": self.deterministic_evidence_hash,
            "mutates_records": self.mutates_records,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
        }
