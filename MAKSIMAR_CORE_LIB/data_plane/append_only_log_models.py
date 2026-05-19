from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class AppendOnlyRecordKind(str, Enum):
    OPERATION = "operation"
    SECURITY_DECISION = "security_decision"
    DATA_PLANE_EVENT = "data_plane_event"
    LEDGER_ANCHOR = "ledger_anchor"


class AppendOnlyMutationIntent(str, Enum):
    APPEND = "append"
    OVERWRITE = "overwrite"
    DELETE = "delete"
    TRUNCATE = "truncate"


@dataclass(frozen=True, slots=True)
class AppendOnlyLogRecord:
    record_id: str
    stream_id: str
    sequence_number: int
    record_kind: AppendOnlyRecordKind
    payload_ref: str
    payload_sha256: str
    producer_layer_id: str
    trace_id: str
    created_at_utc: str
    previous_record_hash: str
    record_hash: str
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    overwrite_allowed: bool = False
    delete_allowed: bool = False
    truncate_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("record_id", self.record_id),
            ("stream_id", self.stream_id),
            ("payload_ref", self.payload_ref),
            ("payload_sha256", self.payload_sha256),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
            ("created_at_utc", self.created_at_utc),
            ("previous_record_hash", self.previous_record_hash),
            ("record_hash", self.record_hash),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.sequence_number < 0:
            raise ValueError("sequence_number must not be negative")

        if not isinstance(self.record_kind, AppendOnlyRecordKind):
            raise TypeError("record_kind must be AppendOnlyRecordKind")

        for field_name, value in (
            ("payload_sha256", self.payload_sha256),
            ("previous_record_hash", self.previous_record_hash),
            ("record_hash", self.record_hash),
        ):
            if len(value) != 64:
                raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
            try:
                int(value, 16)
            except ValueError as exc:
                raise ValueError(f"{field_name} must be hex encoded") from exc

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.overwrite_allowed:
            raise ValueError("overwrite_allowed must remain false")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.truncate_allowed:
            raise ValueError("truncate_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["record_kind"] = self.record_kind.value
        return payload


@dataclass(frozen=True, slots=True)
class AppendOnlyLogStream:
    stream_id: str
    records: tuple[AppendOnlyLogRecord, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    overwrite_allowed: bool = False
    delete_allowed: bool = False
    truncate_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.stream_id:
            raise ValueError("stream_id must not be empty")
        if not isinstance(self.records, tuple):
            raise TypeError("records must be a tuple")
        for record in self.records:
            if not isinstance(record, AppendOnlyLogRecord):
                raise TypeError("records must contain AppendOnlyLogRecord")
            if record.stream_id != self.stream_id:
                raise ValueError("all records must belong to stream_id")

        expected_sequence = 0
        previous_hash = "0" * 64
        seen_ids: set[str] = set()

        for record in self.records:
            if record.record_id in seen_ids:
                raise ValueError("record_id values must be unique")
            seen_ids.add(record.record_id)

            if record.sequence_number != expected_sequence:
                raise ValueError("records must be contiguous and ordered by sequence_number")
            if record.previous_record_hash != previous_hash:
                raise ValueError("record previous_record_hash must match prior record_hash")

            expected_sequence += 1
            previous_hash = record.record_hash

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.overwrite_allowed:
            raise ValueError("overwrite_allowed must remain false")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.truncate_allowed:
            raise ValueError("truncate_allowed must remain false")

    @property
    def next_sequence_number(self) -> int:
        return len(self.records)

    @property
    def head_hash(self) -> str:
        if not self.records:
            return "0" * 64
        return self.records[-1].record_hash

    def to_dict(self) -> dict[str, Any]:
        return {
            "stream_id": self.stream_id,
            "records": [record.to_dict() for record in self.records],
            "next_sequence_number": self.next_sequence_number,
            "head_hash": self.head_hash,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "overwrite_allowed": self.overwrite_allowed,
            "delete_allowed": self.delete_allowed,
            "truncate_allowed": self.truncate_allowed,
        }


@dataclass(frozen=True, slots=True)
class AppendOnlyLogReadModel:
    stream_id: str
    record_count: int
    head_hash: str
    append_only_enforced: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    overwrite_allowed: bool = False
    delete_allowed: bool = False
    truncate_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.stream_id:
            raise ValueError("stream_id must not be empty")
        if self.record_count < 0:
            raise ValueError("record_count must not be negative")
        if not self.head_hash:
            raise ValueError("head_hash must not be empty")
        if len(self.head_hash) != 64:
            raise ValueError("head_hash must be a 64-character sha256 hex string")
        int(self.head_hash, 16)

        if not self.append_only_enforced:
            raise ValueError("append_only_enforced must remain true")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.overwrite_allowed:
            raise ValueError("overwrite_allowed must remain false")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.truncate_allowed:
            raise ValueError("truncate_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
