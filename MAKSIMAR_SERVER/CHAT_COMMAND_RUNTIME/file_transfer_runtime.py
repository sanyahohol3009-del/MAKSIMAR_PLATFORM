from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.chat_command.file_transfer_contract import FileTransferContract


_ALLOWED_RUNTIME_STATES = ("planned_reference", "blocked", "completed_reference")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class FileTransferRuntimeRecord:
    transfer_id: str
    message_id: str
    attachment_id: str
    runtime_state: str
    checksum_required: bool
    encryption_required: bool
    direct_file_system_write_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "transfer_id", _ensure_non_empty(self.transfer_id, "transfer_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))

        if self.runtime_state not in _ALLOWED_RUNTIME_STATES:
            raise ValueError(f"runtime_state must be one of {_ALLOWED_RUNTIME_STATES}: {self.runtime_state}")
        if not self.checksum_required:
            raise ValueError("checksum_required must be True")
        if not self.encryption_required:
            raise ValueError("encryption_required must be True")
        if self.direct_file_system_write_allowed:
            raise ValueError("direct_file_system_write_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")


@dataclass
class FileTransferRuntime:
    """In-memory file transfer runtime.

    It creates transfer records only. It does not copy files, write files,
    open network connections, upload/download data, or mutate canonical state.
    """

    _records: Dict[str, FileTransferRuntimeRecord] = field(default_factory=dict)

    def plan_transfer(self, contract: FileTransferContract) -> FileTransferRuntimeRecord:
        if contract.transfer_id in self._records:
            raise ValueError(f"transfer already planned: {contract.transfer_id}")

        record = FileTransferRuntimeRecord(
            transfer_id=contract.transfer_id,
            message_id=contract.message_id,
            attachment_id=contract.attachment_id,
            runtime_state="planned_reference",
            checksum_required=True,
            encryption_required=True,
            direct_file_system_write_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[record.transfer_id] = record
        return record

    def mark_completed_reference(self, transfer_id: str) -> FileTransferRuntimeRecord:
        current = self.get_record(transfer_id)
        completed = FileTransferRuntimeRecord(
            transfer_id=current.transfer_id,
            message_id=current.message_id,
            attachment_id=current.attachment_id,
            runtime_state="completed_reference",
            checksum_required=True,
            encryption_required=True,
            direct_file_system_write_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[transfer_id] = completed
        return completed

    def get_record(self, transfer_id: str) -> FileTransferRuntimeRecord:
        transfer_id = _ensure_non_empty(transfer_id, "transfer_id")
        try:
            return self._records[transfer_id]
        except KeyError as exc:
            raise KeyError(f"unknown file transfer: {transfer_id}") from exc

    def list_records(self) -> Tuple[FileTransferRuntimeRecord, ...]:
        return tuple(self._records.values())
