from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.append_only_log_models import (
    AppendOnlyLogRecord,
    AppendOnlyLogStream,
    AppendOnlyRecordKind,
)

ZERO = "0" * 64
ONE = "1" * 64
TWO = "2" * 64


def test_append_only_log_stream_accepts_hash_chained_records() -> None:
    record = AppendOnlyLogRecord(
        record_id="stream:00000000000000000000",
        stream_id="stream",
        sequence_number=0,
        record_kind=AppendOnlyRecordKind.OPERATION,
        payload_ref="object://payload/1",
        payload_sha256=ONE,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-1",
        created_at_utc="2026-01-01T00:00:00Z",
        previous_record_hash=ZERO,
        record_hash=TWO,
    )

    stream = AppendOnlyLogStream(stream_id="stream", records=(record,))

    assert stream.next_sequence_number == 1
    assert stream.head_hash == TWO
    assert stream.dashboard_safe is True
    assert stream.overwrite_allowed is False
    assert stream.delete_allowed is False
    assert stream.truncate_allowed is False


def test_append_only_log_rejects_broken_sequence() -> None:
    record = AppendOnlyLogRecord(
        record_id="stream:00000000000000000001",
        stream_id="stream",
        sequence_number=1,
        record_kind=AppendOnlyRecordKind.OPERATION,
        payload_ref="object://payload/1",
        payload_sha256=ONE,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-1",
        created_at_utc="2026-01-01T00:00:00Z",
        previous_record_hash=ZERO,
        record_hash=TWO,
    )

    with pytest.raises(ValueError, match="contiguous"):
        AppendOnlyLogStream(stream_id="stream", records=(record,))


def test_append_only_log_record_rejects_mutation_flags() -> None:
    with pytest.raises(ValueError, match="overwrite_allowed"):
        AppendOnlyLogRecord(
            record_id="stream:00000000000000000000",
            stream_id="stream",
            sequence_number=0,
            record_kind=AppendOnlyRecordKind.OPERATION,
            payload_ref="object://payload/1",
            payload_sha256=ONE,
            producer_layer_id="CONTROL_PLANE",
            trace_id="trace-1",
            created_at_utc="2026-01-01T00:00:00Z",
            previous_record_hash=ZERO,
            record_hash=TWO,
            overwrite_allowed=True,
        )
