from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.data_plane.append_only_log_models import (
    AppendOnlyLogReadModel,
    AppendOnlyLogRecord,
    AppendOnlyLogStream,
    AppendOnlyMutationIntent,
    AppendOnlyRecordKind,
)


@dataclass(frozen=True, slots=True)
class AppendOnlyLogAppendRequest:
    request_id: str
    stream_id: str
    record_kind: AppendOnlyRecordKind
    payload_ref: str
    payload_sha256: str
    producer_layer_id: str
    trace_id: str
    created_at_utc: str
    mutation_intent: AppendOnlyMutationIntent = AppendOnlyMutationIntent.APPEND

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("stream_id", self.stream_id),
            ("payload_ref", self.payload_ref),
            ("payload_sha256", self.payload_sha256),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
            ("created_at_utc", self.created_at_utc),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.record_kind, AppendOnlyRecordKind):
            raise TypeError("record_kind must be AppendOnlyRecordKind")
        if not isinstance(self.mutation_intent, AppendOnlyMutationIntent):
            raise TypeError("mutation_intent must be AppendOnlyMutationIntent")
        if len(self.payload_sha256) != 64:
            raise ValueError("payload_sha256 must be a 64-character sha256 hex string")
        int(self.payload_sha256, 16)


@dataclass(frozen=True, slots=True)
class AppendOnlyLogAppendDecision:
    request_id: str
    accepted: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    overwrite_allowed: bool = False
    delete_allowed: bool = False
    truncate_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.accepted and self.reason_codes != ("append_only_request_accepted",):
            raise ValueError("accepted append decision requires append_only_request_accepted reason")
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


@dataclass(frozen=True, slots=True)
class AppendOnlyLogAppendResult:
    decision: AppendOnlyLogAppendDecision
    stream: AppendOnlyLogStream
    appended_record: AppendOnlyLogRecord | None

    def __post_init__(self) -> None:
        if not isinstance(self.decision, AppendOnlyLogAppendDecision):
            raise TypeError("decision must be AppendOnlyLogAppendDecision")
        if not isinstance(self.stream, AppendOnlyLogStream):
            raise TypeError("stream must be AppendOnlyLogStream")
        if self.appended_record is not None and not isinstance(self.appended_record, AppendOnlyLogRecord):
            raise TypeError("appended_record must be AppendOnlyLogRecord or None")
        if self.decision.accepted and self.appended_record is None:
            raise ValueError("accepted append result requires appended_record")
        if not self.decision.accepted and self.appended_record is not None:
            raise ValueError("rejected append result must not include appended_record")


def calculate_append_only_record_hash(
    *,
    record_id: str,
    stream_id: str,
    sequence_number: int,
    record_kind: AppendOnlyRecordKind,
    payload_ref: str,
    payload_sha256: str,
    producer_layer_id: str,
    trace_id: str,
    created_at_utc: str,
    previous_record_hash: str,
) -> str:
    material: dict[str, Any] = {
        "record_id": record_id,
        "stream_id": stream_id,
        "sequence_number": sequence_number,
        "record_kind": record_kind.value,
        "payload_ref": payload_ref,
        "payload_sha256": payload_sha256,
        "producer_layer_id": producer_layer_id,
        "trace_id": trace_id,
        "created_at_utc": created_at_utc,
        "previous_record_hash": previous_record_hash,
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def reject_non_append_intent(request: AppendOnlyLogAppendRequest) -> AppendOnlyLogAppendDecision:
    if request.mutation_intent is AppendOnlyMutationIntent.APPEND:
        return AppendOnlyLogAppendDecision(
            request_id=request.request_id,
            accepted=True,
            reason_codes=("append_only_request_accepted",),
        )

    return AppendOnlyLogAppendDecision(
        request_id=request.request_id,
        accepted=False,
        reason_codes=(f"{request.mutation_intent.value}_intent_rejected_by_append_only_contract",),
    )


def append_record_to_stream(
    *,
    stream: AppendOnlyLogStream,
    request: AppendOnlyLogAppendRequest,
) -> AppendOnlyLogAppendResult:
    if stream.stream_id != request.stream_id:
        raise ValueError("request stream_id must match stream stream_id")

    decision = reject_non_append_intent(request)
    if not decision.accepted:
        return AppendOnlyLogAppendResult(
            decision=decision,
            stream=stream,
            appended_record=None,
        )

    sequence_number = stream.next_sequence_number
    previous_record_hash = stream.head_hash
    record_id = f"{request.stream_id}:{sequence_number:020d}"

    record_hash = calculate_append_only_record_hash(
        record_id=record_id,
        stream_id=request.stream_id,
        sequence_number=sequence_number,
        record_kind=request.record_kind,
        payload_ref=request.payload_ref,
        payload_sha256=request.payload_sha256,
        producer_layer_id=request.producer_layer_id,
        trace_id=request.trace_id,
        created_at_utc=request.created_at_utc,
        previous_record_hash=previous_record_hash,
    )

    appended_record = AppendOnlyLogRecord(
        record_id=record_id,
        stream_id=request.stream_id,
        sequence_number=sequence_number,
        record_kind=request.record_kind,
        payload_ref=request.payload_ref,
        payload_sha256=request.payload_sha256,
        producer_layer_id=request.producer_layer_id,
        trace_id=request.trace_id,
        created_at_utc=request.created_at_utc,
        previous_record_hash=previous_record_hash,
        record_hash=record_hash,
    )

    new_stream = AppendOnlyLogStream(
        stream_id=stream.stream_id,
        records=stream.records + (appended_record,),
    )

    return AppendOnlyLogAppendResult(
        decision=decision,
        stream=new_stream,
        appended_record=appended_record,
    )


def build_append_only_log_read_model(stream: AppendOnlyLogStream) -> AppendOnlyLogReadModel:
    return AppendOnlyLogReadModel(
        stream_id=stream.stream_id,
        record_count=len(stream.records),
        head_hash=stream.head_hash,
        append_only_enforced=True,
        reason_codes=("append_only_log_contract_enforced",),
    )
