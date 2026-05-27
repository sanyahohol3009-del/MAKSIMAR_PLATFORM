from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.chat_command.server_sync_contract import ServerSyncContract


_ALLOWED_SYNC_RUNTIME_STATES = ("planned_reference", "blocked", "completed_reference")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class ServerToServerSyncRuntimeRecord:
    sync_id: str
    source_node_id: str
    target_node_id: str
    sync_scope: str
    runtime_state: str
    encryption_required: bool
    operator_approval_required: bool
    direct_sync_execution_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "sync_id", _ensure_non_empty(self.sync_id, "sync_id"))
        object.__setattr__(self, "source_node_id", _ensure_non_empty(self.source_node_id, "source_node_id"))
        object.__setattr__(self, "target_node_id", _ensure_non_empty(self.target_node_id, "target_node_id"))
        object.__setattr__(self, "sync_scope", _ensure_non_empty(self.sync_scope, "sync_scope"))

        if self.runtime_state not in _ALLOWED_SYNC_RUNTIME_STATES:
            raise ValueError(f"runtime_state must be one of {_ALLOWED_SYNC_RUNTIME_STATES}: {self.runtime_state}")
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


@dataclass
class ServerToServerSyncRuntime:
    """In-memory server-to-server sync runtime.

    It plans sync references only. It does not replicate data, open network
    connections, write remote state, or start server sync workers.
    """

    _records: Dict[str, ServerToServerSyncRuntimeRecord] = field(default_factory=dict)

    def plan_sync(self, contract: ServerSyncContract) -> ServerToServerSyncRuntimeRecord:
        if contract.sync_id in self._records:
            raise ValueError(f"sync already planned: {contract.sync_id}")

        record = ServerToServerSyncRuntimeRecord(
            sync_id=contract.sync_id,
            source_node_id=contract.source_node_id,
            target_node_id=contract.target_node_id,
            sync_scope=contract.sync_scope,
            runtime_state="planned_reference",
            encryption_required=True,
            operator_approval_required=True,
            direct_sync_execution_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[record.sync_id] = record
        return record

    def mark_completed_reference(self, sync_id: str) -> ServerToServerSyncRuntimeRecord:
        current = self.get_record(sync_id)
        completed = ServerToServerSyncRuntimeRecord(
            sync_id=current.sync_id,
            source_node_id=current.source_node_id,
            target_node_id=current.target_node_id,
            sync_scope=current.sync_scope,
            runtime_state="completed_reference",
            encryption_required=True,
            operator_approval_required=True,
            direct_sync_execution_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[sync_id] = completed
        return completed

    def get_record(self, sync_id: str) -> ServerToServerSyncRuntimeRecord:
        sync_id = _ensure_non_empty(sync_id, "sync_id")
        try:
            return self._records[sync_id]
        except KeyError as exc:
            raise KeyError(f"unknown server sync: {sync_id}") from exc

    def list_records(self) -> Tuple[ServerToServerSyncRuntimeRecord, ...]:
        return tuple(self._records.values())
