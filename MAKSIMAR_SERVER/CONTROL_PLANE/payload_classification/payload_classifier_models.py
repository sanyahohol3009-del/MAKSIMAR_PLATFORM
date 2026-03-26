from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    PayloadClass,
    PayloadDirection,
)


@dataclass(frozen=True, slots=True)
class ServerPayloadClassificationEntry:
    """Server-side payload classification entry."""

    request_id: str
    payload_size_kb: int
    detected_payload_class: PayloadClass
    route_target: PayloadDirection
    inline_allowed: bool
    valid: bool
    classification_reason: str


@dataclass(frozen=True, slots=True)
class ServerPayloadClassificationContract:
    """Unified server-side payload classification contract."""

    total_entries: int
    entries: tuple[ServerPayloadClassificationEntry, ...]
