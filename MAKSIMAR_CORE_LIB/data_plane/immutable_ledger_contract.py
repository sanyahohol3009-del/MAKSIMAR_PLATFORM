from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.data_plane.immutable_ledger_models import (
    ImmutableLedger,
    ImmutableLedgerEntry,
    ImmutableLedgerEntryKind,
    ImmutableLedgerReadModel,
)


@dataclass(frozen=True, slots=True)
class ImmutableLedgerAppendRequest:
    request_id: str
    ledger_id: str
    entry_kind: ImmutableLedgerEntryKind
    anchor_ref: str
    anchor_hash: str
    created_at_utc: str
    producer_layer_id: str
    trace_id: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("ledger_id", self.ledger_id),
            ("anchor_ref", self.anchor_ref),
            ("anchor_hash", self.anchor_hash),
            ("created_at_utc", self.created_at_utc),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.entry_kind, ImmutableLedgerEntryKind):
            raise TypeError("entry_kind must be ImmutableLedgerEntryKind")
        if len(self.anchor_hash) != 64:
            raise ValueError("anchor_hash must be a 64-character sha256 hex string")
        int(self.anchor_hash, 16)


@dataclass(frozen=True, slots=True)
class ImmutableLedgerAppendDecision:
    request_id: str
    accepted: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    mutation_allowed: bool = False
    delete_allowed: bool = False
    overwrite_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.accepted and self.reason_codes != ("immutable_ledger_append_accepted",):
            raise ValueError("accepted ledger decision requires immutable_ledger_append_accepted reason")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.mutation_allowed:
            raise ValueError("mutation_allowed must remain false")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.overwrite_allowed:
            raise ValueError("overwrite_allowed must remain false")


@dataclass(frozen=True, slots=True)
class ImmutableLedgerAppendResult:
    decision: ImmutableLedgerAppendDecision
    ledger: ImmutableLedger
    appended_entry: ImmutableLedgerEntry

    def __post_init__(self) -> None:
        if not isinstance(self.decision, ImmutableLedgerAppendDecision):
            raise TypeError("decision must be ImmutableLedgerAppendDecision")
        if not isinstance(self.ledger, ImmutableLedger):
            raise TypeError("ledger must be ImmutableLedger")
        if not isinstance(self.appended_entry, ImmutableLedgerEntry):
            raise TypeError("appended_entry must be ImmutableLedgerEntry")
        if not self.decision.accepted:
            raise ValueError("immutable ledger append result requires accepted decision")


def calculate_immutable_ledger_entry_hash(
    *,
    ledger_id: str,
    entry_id: str,
    sequence_number: int,
    entry_kind: ImmutableLedgerEntryKind,
    anchor_ref: str,
    anchor_hash: str,
    previous_entry_hash: str,
    created_at_utc: str,
    producer_layer_id: str,
    trace_id: str,
) -> str:
    material: dict[str, Any] = {
        "ledger_id": ledger_id,
        "entry_id": entry_id,
        "sequence_number": sequence_number,
        "entry_kind": entry_kind.value,
        "anchor_ref": anchor_ref,
        "anchor_hash": anchor_hash,
        "previous_entry_hash": previous_entry_hash,
        "created_at_utc": created_at_utc,
        "producer_layer_id": producer_layer_id,
        "trace_id": trace_id,
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def append_ledger_entry(
    *,
    ledger: ImmutableLedger,
    request: ImmutableLedgerAppendRequest,
) -> ImmutableLedgerAppendResult:
    if ledger.ledger_id != request.ledger_id:
        raise ValueError("request ledger_id must match ledger ledger_id")

    sequence_number = ledger.next_sequence_number
    previous_entry_hash = ledger.head_hash
    entry_id = f"{request.ledger_id}:{sequence_number:020d}"

    entry_hash = calculate_immutable_ledger_entry_hash(
        ledger_id=request.ledger_id,
        entry_id=entry_id,
        sequence_number=sequence_number,
        entry_kind=request.entry_kind,
        anchor_ref=request.anchor_ref,
        anchor_hash=request.anchor_hash,
        previous_entry_hash=previous_entry_hash,
        created_at_utc=request.created_at_utc,
        producer_layer_id=request.producer_layer_id,
        trace_id=request.trace_id,
    )

    entry = ImmutableLedgerEntry(
        ledger_id=request.ledger_id,
        entry_id=entry_id,
        sequence_number=sequence_number,
        entry_kind=request.entry_kind,
        anchor_ref=request.anchor_ref,
        anchor_hash=request.anchor_hash,
        previous_entry_hash=previous_entry_hash,
        entry_hash=entry_hash,
        created_at_utc=request.created_at_utc,
        producer_layer_id=request.producer_layer_id,
        trace_id=request.trace_id,
    )

    new_ledger = ImmutableLedger(
        ledger_id=ledger.ledger_id,
        entries=ledger.entries + (entry,),
    )

    return ImmutableLedgerAppendResult(
        decision=ImmutableLedgerAppendDecision(
            request_id=request.request_id,
            accepted=True,
            reason_codes=("immutable_ledger_append_accepted",),
        ),
        ledger=new_ledger,
        appended_entry=entry,
    )


def build_immutable_ledger_read_model(ledger: ImmutableLedger) -> ImmutableLedgerReadModel:
    return ImmutableLedgerReadModel(
        ledger_id=ledger.ledger_id,
        entry_count=len(ledger.entries),
        head_hash=ledger.head_hash,
        immutable_enforced=True,
        reason_codes=("immutable_ledger_contract_enforced",),
    )
