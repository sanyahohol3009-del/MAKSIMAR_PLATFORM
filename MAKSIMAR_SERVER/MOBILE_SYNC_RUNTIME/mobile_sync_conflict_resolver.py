from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared_mobile_core.mobile_sync_models.mobile_sync_conflict_contract import MobileSyncConflictContract


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class MobileSyncConflictResolution:
    resolution_id: str
    conflict: MobileSyncConflictContract
    deterministic: bool
    evidence_hash: str
    success_requires_evidence: bool
    silent_success_allowed: bool
    mutates_records: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_connection_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "resolution_id", _ensure_non_empty(self.resolution_id, "resolution_id"))
        object.__setattr__(self, "evidence_hash", _ensure_non_empty(self.evidence_hash, "evidence_hash"))

        if not isinstance(self.conflict, MobileSyncConflictContract):
            raise ValueError("conflict must be MobileSyncConflictContract")
        if self.evidence_hash != self.conflict.deterministic_evidence_hash:
            raise ValueError("evidence_hash must match conflict deterministic_evidence_hash")
        if self.deterministic is not True:
            raise ValueError("deterministic must be True")
        if self.success_requires_evidence is not True:
            raise ValueError("success_requires_evidence must be True")
        if self.silent_success_allowed is not False:
            raise ValueError("silent_success_allowed must be False")

        required_false = {
            "mutates_records": self.mutates_records,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_connection_allowed": self.runtime_connection_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "resolution_id": self.resolution_id,
            "conflict_id": self.conflict.conflict_id,
            "memory_domain": self.conflict.memory_domain,
            "decision": self.conflict.decision,
            "decision_reason": self.conflict.decision_reason,
            "evidence_hash": self.evidence_hash,
            "deterministic": self.deterministic,
            "success_requires_evidence": self.success_requires_evidence,
            "silent_success_allowed": self.silent_success_allowed,
            "mutates_records": self.mutates_records,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
        }


@dataclass(frozen=True)
class MobileSyncConflictResolver:
    resolver_id: str
    deterministic_only: bool
    read_only_runtime: bool
    mutates_records: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_connection_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "resolver_id", _ensure_non_empty(self.resolver_id, "resolver_id"))
        if self.deterministic_only is not True:
            raise ValueError("deterministic_only must be True")
        if self.read_only_runtime is not True:
            raise ValueError("read_only_runtime must be True")

        required_false = {
            "mutates_records": self.mutates_records,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_connection_allowed": self.runtime_connection_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default(cls, *, resolver_id: str) -> "MobileSyncConflictResolver":
        return cls(
            resolver_id=resolver_id,
            deterministic_only=True,
            read_only_runtime=True,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
        )

    def resolve(
        self,
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
    ) -> MobileSyncConflictResolution:
        conflict = MobileSyncConflictContract.decide(
            conflict_id=conflict_id,
            memory_domain=memory_domain,
            local_record_ref=local_record_ref,
            server_record_ref=server_record_ref,
            local_sequence=local_sequence,
            server_sequence=server_sequence,
            local_updated_at_epoch_ms=local_updated_at_epoch_ms,
            server_updated_at_epoch_ms=server_updated_at_epoch_ms,
            conflict_policy_ref=conflict_policy_ref,
        )
        return MobileSyncConflictResolution(
            resolution_id=f"{self.resolver_id}:{conflict.conflict_id}",
            conflict=conflict,
            deterministic=True,
            evidence_hash=conflict.deterministic_evidence_hash,
            success_requires_evidence=True,
            silent_success_allowed=False,
            mutates_records=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
        )
