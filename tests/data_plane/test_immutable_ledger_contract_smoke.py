from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_contract import (
    ImmutableLedgerAppendRequest,
    append_ledger_entry,
    build_immutable_ledger_read_model,
)
from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_models import (
    ImmutableLedger,
    ImmutableLedgerEntryKind,
)

ONE = "1" * 64


def test_immutable_ledger_contract_appends_entry() -> None:
    ledger = ImmutableLedger(ledger_id="ledger", entries=())
    request = ImmutableLedgerAppendRequest(
        request_id="req-1",
        ledger_id="ledger",
        entry_kind=ImmutableLedgerEntryKind.APPEND_LOG_ANCHOR,
        anchor_ref="append-log://stream/0",
        anchor_hash=ONE,
        created_at_utc="2026-01-01T00:00:00Z",
        producer_layer_id="DATA_PLANE",
        trace_id="trace-1",
    )

    result = append_ledger_entry(ledger=ledger, request=request)
    read_model = build_immutable_ledger_read_model(result.ledger)

    assert result.decision.accepted is True
    assert result.appended_entry.sequence_number == 0
    assert read_model.immutable_enforced is True
    assert read_model.mutation_allowed is False
    assert read_model.delete_allowed is False
    assert read_model.overwrite_allowed is False
