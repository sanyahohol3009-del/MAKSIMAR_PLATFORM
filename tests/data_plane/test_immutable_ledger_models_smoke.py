from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_models import (
    ImmutableLedger,
    ImmutableLedgerEntry,
    ImmutableLedgerEntryKind,
)

ZERO = "0" * 64
ONE = "1" * 64
TWO = "2" * 64


def test_immutable_ledger_accepts_hash_chained_entries() -> None:
    entry = ImmutableLedgerEntry(
        ledger_id="ledger",
        entry_id="ledger:00000000000000000000",
        sequence_number=0,
        entry_kind=ImmutableLedgerEntryKind.APPEND_LOG_ANCHOR,
        anchor_ref="append-log://stream/0",
        anchor_hash=ONE,
        previous_entry_hash=ZERO,
        entry_hash=TWO,
        created_at_utc="2026-01-01T00:00:00Z",
        producer_layer_id="DATA_PLANE",
        trace_id="trace-1",
    )

    ledger = ImmutableLedger(ledger_id="ledger", entries=(entry,))

    assert ledger.next_sequence_number == 1
    assert ledger.head_hash == TWO
    assert ledger.mutation_allowed is False
    assert ledger.delete_allowed is False
    assert ledger.overwrite_allowed is False


def test_immutable_ledger_rejects_mutation_flags() -> None:
    with pytest.raises(ValueError, match="mutation_allowed"):
        ImmutableLedgerEntry(
            ledger_id="ledger",
            entry_id="ledger:00000000000000000000",
            sequence_number=0,
            entry_kind=ImmutableLedgerEntryKind.APPEND_LOG_ANCHOR,
            anchor_ref="append-log://stream/0",
            anchor_hash=ONE,
            previous_entry_hash=ZERO,
            entry_hash=TWO,
            created_at_utc="2026-01-01T00:00:00Z",
            producer_layer_id="DATA_PLANE",
            trace_id="trace-1",
            mutation_allowed=True,
        )
