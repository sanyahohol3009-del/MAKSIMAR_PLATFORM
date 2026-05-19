from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.append_only_log_contract import (
    AppendOnlyLogAppendRequest,
    append_record_to_stream,
)
from MAKSIMAR_CORE_LIB.data_plane.append_only_log_models import (
    AppendOnlyLogStream,
    AppendOnlyMutationIntent,
    AppendOnlyRecordKind,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_semantic_duplicate_binding import (
    BATCH_2_2_SEMANTIC_DUPLICATE_BINDING,
)

ONE = "1" * 64


def test_data_plane_append_contract_blocks_delete_and_overwrite() -> None:
    stream = AppendOnlyLogStream(stream_id="stream", records=())

    rejected_intents = (
        AppendOnlyMutationIntent.OVERWRITE,
        AppendOnlyMutationIntent.DELETE,
        AppendOnlyMutationIntent.TRUNCATE,
    )

    for intent in rejected_intents:
        request = AppendOnlyLogAppendRequest(
            request_id=f"req-{intent.value}",
            stream_id="stream",
            record_kind=AppendOnlyRecordKind.DATA_PLANE_EVENT,
            payload_ref="object://payload/1",
            payload_sha256=ONE,
            producer_layer_id="DATA_PLANE",
            trace_id="trace-1",
            created_at_utc="2026-01-01T00:00:00Z",
            mutation_intent=intent,
        )

        result = append_record_to_stream(stream=stream, request=request)

        assert result.decision.accepted is False
        assert result.stream.records == ()
        assert result.decision.canonical_write_allowed is False
        assert result.decision.delete_allowed is False
        assert result.decision.overwrite_allowed is False


def test_data_plane_semantic_duplicate_binding_is_safe() -> None:
    binding = BATCH_2_2_SEMANTIC_DUPLICATE_BINDING

    assert binding.batch_id == "PHASE_2_BATCH_2_2"
    assert binding.dashboard_safe is True
    assert binding.runtime_mutation_allowed is False
    assert binding.canonical_write_allowed is False
    assert binding.auto_move_allowed is False
    assert binding.auto_delete_allowed is False
