from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class ImmutableLedgerEntryKind(str, Enum):
    APPEND_LOG_ANCHOR = "append_log_anchor"
    SECURITY_ANCHOR = "security_anchor"
    ARTIFACT_ANCHOR = "artifact_anchor"
    DATA_PLANE_ANCHOR = "data_plane_anchor"


@dataclass(frozen=True, slots=True)
class ImmutableLedgerEntry:
    ledger_id: str
    entry_id: str
    sequence_number: int
    entry_kind: ImmutableLedgerEntryKind
    anchor_ref: str
    anchor_hash: str
    previous_entry_hash: str
    entry_hash: str
    created_at_utc: str
    producer_layer_id: str
    trace_id: str
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    mutation_allowed: bool = False
    delete_allowed: bool = False
    overwrite_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("ledger_id", self.ledger_id),
            ("entry_id", self.entry_id),
            ("anchor_ref", self.anchor_ref),
            ("anchor_hash", self.anchor_hash),
            ("previous_entry_hash", self.previous_entry_hash),
            ("entry_hash", self.entry_hash),
            ("created_at_utc", self.created_at_utc),
            ("producer_layer_id", self.producer_layer_id),
            ("trace_id", self.trace_id),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if self.sequence_number < 0:
            raise ValueError("sequence_number must not be negative")

        if not isinstance(self.entry_kind, ImmutableLedgerEntryKind):
            raise TypeError("entry_kind must be ImmutableLedgerEntryKind")

        for field_name, value in (
            ("anchor_hash", self.anchor_hash),
            ("previous_entry_hash", self.previous_entry_hash),
            ("entry_hash", self.entry_hash),
        ):
            if len(value) != 64:
                raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
            int(value, 16)

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

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["entry_kind"] = self.entry_kind.value
        return payload


@dataclass(frozen=True, slots=True)
class ImmutableLedger:
    ledger_id: str
    entries: tuple[ImmutableLedgerEntry, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    mutation_allowed: bool = False
    delete_allowed: bool = False
    overwrite_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("ledger_id must not be empty")
        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be a tuple")

        expected_sequence = 0
        previous_hash = "0" * 64
        seen_ids: set[str] = set()

        for entry in self.entries:
            if not isinstance(entry, ImmutableLedgerEntry):
                raise TypeError("entries must contain ImmutableLedgerEntry")
            if entry.ledger_id != self.ledger_id:
                raise ValueError("all entries must belong to ledger_id")
            if entry.entry_id in seen_ids:
                raise ValueError("entry_id values must be unique")
            seen_ids.add(entry.entry_id)
            if entry.sequence_number != expected_sequence:
                raise ValueError("ledger entries must be contiguous and ordered by sequence_number")
            if entry.previous_entry_hash != previous_hash:
                raise ValueError("entry previous_entry_hash must match prior entry_hash")
            expected_sequence += 1
            previous_hash = entry.entry_hash

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

    @property
    def next_sequence_number(self) -> int:
        return len(self.entries)

    @property
    def head_hash(self) -> str:
        if not self.entries:
            return "0" * 64
        return self.entries[-1].entry_hash

    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_id": self.ledger_id,
            "entries": [entry.to_dict() for entry in self.entries],
            "next_sequence_number": self.next_sequence_number,
            "head_hash": self.head_hash,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "mutation_allowed": self.mutation_allowed,
            "delete_allowed": self.delete_allowed,
            "overwrite_allowed": self.overwrite_allowed,
        }


@dataclass(frozen=True, slots=True)
class ImmutableLedgerReadModel:
    ledger_id: str
    entry_count: int
    head_hash: str
    immutable_enforced: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    mutation_allowed: bool = False
    delete_allowed: bool = False
    overwrite_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.ledger_id:
            raise ValueError("ledger_id must not be empty")
        if self.entry_count < 0:
            raise ValueError("entry_count must not be negative")
        if not self.head_hash:
            raise ValueError("head_hash must not be empty")
        if len(self.head_hash) != 64:
            raise ValueError("head_hash must be a 64-character sha256 hex string")
        int(self.head_hash, 16)
        if not self.immutable_enforced:
            raise ValueError("immutable_enforced must remain true")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
