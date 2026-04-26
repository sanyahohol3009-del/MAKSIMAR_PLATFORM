from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_routing_contract import (
    build_voice_routing_contract,
)


VoiceDisplayTarget = Literal[
    "display_operator_interaction",
    "display_foundation_secondary",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VoiceDisplayHandoffEntry:
    handoff_entry_id: str
    routing_entry_id: str
    display_target_id: VoiceDisplayTarget
    display_handoff_ready: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.handoff_entry_id, "handoff_entry_id")
        _require_non_empty(self.routing_entry_id, "routing_entry_id")
        _require_non_empty(self.description, "description")

        if not self.display_handoff_ready:
            raise ValueError(
                "display_handoff_ready must remain true for canonical voice display handoff entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical voice display handoff entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical voice display handoff entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical voice display handoff entries."
            )


@dataclass(frozen=True, slots=True)
class VoiceDisplayHandoffContract:
    contract_id: str
    total_entries: int
    ready_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VoiceDisplayHandoffEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.ready_entries != sum(
            1 for entry in self.entries if entry.display_handoff_ready
        ):
            raise ValueError("ready_entries must match display_handoff_ready count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError(
                "guarded_entries must match guarded voice display handoff count."
            )
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_voice_display_handoff_contract() -> VoiceDisplayHandoffContract:
    routing_contract = build_voice_routing_contract()
    display_targets: tuple[VoiceDisplayTarget, ...] = (
        "display_operator_interaction",
        "display_foundation_secondary",
        "display_operator_interaction",
    )

    entries = tuple(
        VoiceDisplayHandoffEntry(
            handoff_entry_id=f"voice_display_handoff_{index:03d}",
            routing_entry_id=entry.routing_entry_id,
            display_target_id=display_targets[index - 1],
            display_handoff_ready=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical voice display handoff entry for {entry.routing_entry_id}.",
        )
        for index, entry in enumerate(routing_contract.entries, start=1)
    )

    return VoiceDisplayHandoffContract(
        contract_id="voice_display_handoff_contract_001",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.display_handoff_ready),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
