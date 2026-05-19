from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.append_only_log_contract import (
    AppendOnlyLogAppendRequest,
    append_record_to_stream,
)
from MAKSIMAR_CORE_LIB.data_plane.append_only_log_models import (
    AppendOnlyLogRecord,
    AppendOnlyLogStream,
    AppendOnlyRecordKind,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import DataPlaneAppendLogReadModel


@dataclass(frozen=True, slots=True)
class DataPlaneAppendLogAdapterResult:
    request_id: str
    log_path: str
    write_performed: bool
    appended_record_id: str
    read_model: DataPlaneAppendLogReadModel
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not self.log_path:
            raise ValueError("log_path must not be empty")
        if not self.appended_record_id:
            raise ValueError("appended_record_id must not be empty")
        if not isinstance(self.read_model, DataPlaneAppendLogReadModel):
            raise TypeError("read_model must be DataPlaneAppendLogReadModel")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def append_payload_reference_to_log(
    *,
    log_path: Path,
    stream_id: str,
    payload_reference: DataPlanePayloadReference,
    created_at_utc: str,
) -> DataPlaneAppendLogAdapterResult:
    if not isinstance(payload_reference, DataPlanePayloadReference):
        raise TypeError("payload_reference must be DataPlanePayloadReference")

    request = AppendOnlyLogAppendRequest(
        request_id=f"{stream_id}:append:{payload_reference.reference_id}",
        stream_id=stream_id,
        record_kind=AppendOnlyRecordKind.DATA_PLANE_EVENT,
        payload_ref=payload_reference.uri,
        payload_sha256=payload_reference.sha256,
        producer_layer_id=payload_reference.producer_layer_id,
        trace_id=payload_reference.trace_id,
        created_at_utc=created_at_utc,
    )

    return append_request_to_local_jsonl_log(log_path=log_path, request=request)


def append_request_to_local_jsonl_log(
    *,
    log_path: Path,
    request: AppendOnlyLogAppendRequest,
) -> DataPlaneAppendLogAdapterResult:
    _validate_jsonl_path(log_path)

    stream = _load_stream_from_jsonl(log_path=log_path, stream_id=request.stream_id)
    result = append_record_to_stream(stream=stream, request=request)

    if result.appended_record is None:
        appended_record_id = "append_rejected_no_record"
    else:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as file_obj:
            file_obj.write(json.dumps(result.appended_record.to_dict(), sort_keys=True) + "\n")
        appended_record_id = result.appended_record.record_id

    read_model = DataPlaneAppendLogReadModel(
        append_log_id=f"append_log_adapter:{request.stream_id}",
        stream_id=request.stream_id,
        log_path=str(log_path),
        record_count=len(result.stream.records),
        head_hash=result.stream.head_hash,
        latest_record_id=appended_record_id,
        write_performed=result.appended_record is not None,
        append_only_enforced=True,
        reason_codes=result.decision.reason_codes,
    )

    return DataPlaneAppendLogAdapterResult(
        request_id=request.request_id,
        log_path=str(log_path),
        write_performed=result.appended_record is not None,
        appended_record_id=appended_record_id,
        read_model=read_model,
    )


def _load_stream_from_jsonl(*, log_path: Path, stream_id: str) -> AppendOnlyLogStream:
    if not stream_id:
        raise ValueError("stream_id must not be empty")
    if not log_path.exists():
        return AppendOnlyLogStream(stream_id=stream_id, records=())

    records: list[AppendOnlyLogRecord] = []
    for line_number, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"append log contains blank line at {line_number}")
        payload = json.loads(line)
        records.append(_record_from_dict(payload))

    return AppendOnlyLogStream(stream_id=stream_id, records=tuple(records))


def _record_from_dict(payload: dict[str, object]) -> AppendOnlyLogRecord:
    return AppendOnlyLogRecord(
        record_id=str(payload["record_id"]),
        stream_id=str(payload["stream_id"]),
        sequence_number=int(payload["sequence_number"]),
        record_kind=AppendOnlyRecordKind(str(payload["record_kind"])),
        payload_ref=str(payload["payload_ref"]),
        payload_sha256=str(payload["payload_sha256"]),
        producer_layer_id=str(payload["producer_layer_id"]),
        trace_id=str(payload["trace_id"]),
        created_at_utc=str(payload["created_at_utc"]),
        previous_record_hash=str(payload["previous_record_hash"]),
        record_hash=str(payload["record_hash"]),
    )


def _validate_jsonl_path(path: Path) -> None:
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    if ".." in path.parts:
        raise ValueError("path must not contain parent traversal")
    if path.suffix != ".jsonl":
        raise ValueError("append log path must use .jsonl suffix")
    if path.exists() and path.is_dir():
        raise ValueError("append log path must not be a directory")
