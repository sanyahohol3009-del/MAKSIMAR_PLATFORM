from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import DataPlaneLedgerReadModel
from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_contract import (
    ImmutableLedgerAppendRequest,
    append_ledger_entry,
)
from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_models import (
    ImmutableLedger,
    ImmutableLedgerEntry,
    ImmutableLedgerEntryKind,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import (
    DataPlaneAppendLogAdapterResult,
)


@dataclass(frozen=True, slots=True)
class DataPlaneLedgerAdapterResult:
    request_id: str
    ledger_path: str
    write_performed: bool
    appended_entry_id: str
    read_model: DataPlaneLedgerReadModel
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.ledger_path:
            raise ValueError("ledger_path must not be empty")
        if not self.appended_entry_id:
            raise ValueError("appended_entry_id must not be empty")
        if not isinstance(self.read_model, DataPlaneLedgerReadModel):
            raise TypeError("read_model must be DataPlaneLedgerReadModel")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def anchor_append_log_result_to_ledger(
    *,
    ledger_path: Path,
    ledger_id: str,
    append_result: DataPlaneAppendLogAdapterResult,
    created_at_utc: str,
) -> DataPlaneLedgerAdapterResult:
    if not isinstance(append_result, DataPlaneAppendLogAdapterResult):
        raise TypeError("append_result must be DataPlaneAppendLogAdapterResult")
    if not append_result.write_performed:
        raise ValueError("append_result must contain a written append-log record")

    request = ImmutableLedgerAppendRequest(
        request_id=f"{ledger_id}:anchor:{append_result.appended_record_id}",
        ledger_id=ledger_id,
        entry_kind=ImmutableLedgerEntryKind.APPEND_LOG_ANCHOR,
        anchor_ref=f"append-log://{append_result.read_model.stream_id}/{append_result.appended_record_id}",
        anchor_hash=append_result.read_model.head_hash,
        created_at_utc=created_at_utc,
        producer_layer_id="DATA_PLANE",
        trace_id=append_result.request_id,
    )

    return append_request_to_local_ledger_jsonl(ledger_path=ledger_path, request=request)


def append_request_to_local_ledger_jsonl(
    *,
    ledger_path: Path,
    request: ImmutableLedgerAppendRequest,
) -> DataPlaneLedgerAdapterResult:
    _validate_jsonl_path(ledger_path)

    ledger = _load_ledger_from_jsonl(ledger_path=ledger_path, ledger_id=request.ledger_id)
    result = append_ledger_entry(ledger=ledger, request=request)

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write(json.dumps(result.appended_entry.to_dict(), sort_keys=True) + "\n")

    read_model = DataPlaneLedgerReadModel(
        ledger_adapter_id=f"ledger_adapter:{request.ledger_id}",
        ledger_id=request.ledger_id,
        ledger_path=str(ledger_path),
        entry_count=len(result.ledger.entries),
        head_hash=result.ledger.head_hash,
        latest_entry_id=result.appended_entry.entry_id,
        write_performed=True,
        immutable_ledger_enforced=True,
        reason_codes=result.decision.reason_codes,
    )

    return DataPlaneLedgerAdapterResult(
        request_id=request.request_id,
        ledger_path=str(ledger_path),
        write_performed=True,
        appended_entry_id=result.appended_entry.entry_id,
        read_model=read_model,
    )


def _load_ledger_from_jsonl(*, ledger_path: Path, ledger_id: str) -> ImmutableLedger:
    if not ledger_id:
        raise ValueError("ledger_id must not be empty")
    if not ledger_path.exists():
        return ImmutableLedger(ledger_id=ledger_id, entries=())

    entries: list[ImmutableLedgerEntry] = []
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"ledger contains blank line at {line_number}")
        payload = json.loads(line)
        entries.append(_entry_from_dict(payload))

    return ImmutableLedger(ledger_id=ledger_id, entries=tuple(entries))


def _entry_from_dict(payload: dict[str, object]) -> ImmutableLedgerEntry:
    return ImmutableLedgerEntry(
        ledger_id=str(payload["ledger_id"]),
        entry_id=str(payload["entry_id"]),
        sequence_number=int(payload["sequence_number"]),
        entry_kind=ImmutableLedgerEntryKind(str(payload["entry_kind"])),
        anchor_ref=str(payload["anchor_ref"]),
        anchor_hash=str(payload["anchor_hash"]),
        previous_entry_hash=str(payload["previous_entry_hash"]),
        entry_hash=str(payload["entry_hash"]),
        created_at_utc=str(payload["created_at_utc"]),
        producer_layer_id=str(payload["producer_layer_id"]),
        trace_id=str(payload["trace_id"]),
    )


def _validate_jsonl_path(path: Path) -> None:
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    if ".." in path.parts:
        raise ValueError("path must not contain parent traversal")
    if path.suffix != ".jsonl":
        raise ValueError("ledger path must use .jsonl suffix")
    if path.exists() and path.is_dir():
        raise ValueError("ledger path must not be a directory")
