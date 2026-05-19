from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.append_only_log_contract import (
    AppendOnlyLogAppendRequest,
    append_record_to_stream,
    build_append_only_log_read_model,
)
from MAKSIMAR_CORE_LIB.data_plane.append_only_log_models import (
    AppendOnlyLogStream,
    AppendOnlyMutationIntent,
    AppendOnlyRecordKind,
)

ONE = "1" * 64


def test_append_only_log_contract_appends_record() -> None:
    stream = AppendOnlyLogStream(stream_id="stream", records=())
    request = AppendOnlyLogAppendRequest(
        request_id="req-1",
        stream_id="stream",
        record_kind=AppendOnlyRecordKind.OPERATION,
        payload_ref="object://payload/1",
        payload_sha256=ONE,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-1",
        created_at_utc="2026-01-01T00:00:00Z",
    )

    result = append_record_to_stream(stream=stream, request=request)
    read_model = build_append_only_log_read_model(result.stream)

    assert result.decision.accepted is True
    assert result.appended_record is not None
    assert result.appended_record.sequence_number == 0
    assert read_model.append_only_enforced is True
    assert read_model.overwrite_allowed is False
    assert read_model.delete_allowed is False


def test_append_only_log_contract_rejects_overwrite_delete_truncate() -> None:
    stream = AppendOnlyLogStream(stream_id="stream", records=())

    for intent in (
        AppendOnlyMutationIntent.OVERWRITE,
        AppendOnlyMutationIntent.DELETE,
        AppendOnlyMutationIntent.TRUNCATE,
    ):
        request = AppendOnlyLogAppendRequest(
            request_id=f"req-{intent.value}",
            stream_id="stream",
            record_kind=AppendOnlyRecordKind.OPERATION,
            payload_ref="object://payload/1",
            payload_sha256=ONE,
            producer_layer_id="CONTROL_PLANE",
            trace_id="trace-1",
            created_at_utc="2026-01-01T00:00:00Z",
            mutation_intent=intent,
        )

        result = append_record_to_stream(stream=stream, request=request)

        assert result.decision.accepted is False
        assert result.appended_record is None
        assert result.stream.records == ()
        assert result.decision.overwrite_allowed is False
        assert result.decision.delete_allowed is False
        assert result.decision.truncate_allowed is False
