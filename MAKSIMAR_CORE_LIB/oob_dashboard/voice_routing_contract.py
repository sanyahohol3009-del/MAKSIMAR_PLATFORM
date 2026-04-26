from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_normalization_contract import (
    build_voice_normalization_contract,
)


VoiceRoutingTarget = Literal[
    "panel_operator_main",
    "panel_explainability",
    "panel_command_strip",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VoiceRoutingEntry:
    routing_entry_id: str
    normalization_entry_id: str
    routing_target: VoiceRoutingTarget
    routed: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.routing_entry_id, "routing_entry_id")
        _require_non_empty(self.normalization_entry_id, "normalization_entry_id")
        _require_non_empty(self.description, "description")

        if not self.routed:
            raise ValueError(
                "routed must remain true for canonical voice routing entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical voice routing entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical voice routing entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical voice routing entries."
            )


@dataclass(frozen=True, slots=True)
class VoiceRoutingContract:
    contract_id: str
    total_entries: int
    routed_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VoiceRoutingEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.routed_entries != sum(
            1 for entry in self.entries if entry.routed
        ):
            raise ValueError("routed_entries must match routed count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded voice routing count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_voice_routing_contract() -> VoiceRoutingContract:
    normalization_contract = build_voice_normalization_contract()
    routing_targets: tuple[VoiceRoutingTarget, ...] = (
        "panel_operator_main",
        "panel_explainability",
        "panel_command_strip",
    )

    entries = tuple(
        VoiceRoutingEntry(
            routing_entry_id=f"voice_routing_{index:03d}",
            normalization_entry_id=entry.normalization_entry_id,
            routing_target=routing_targets[index - 1],
            routed=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical voice routing entry for {entry.normalization_entry_id}.",
        )
        for index, entry in enumerate(normalization_contract.entries, start=1)
    )

    return VoiceRoutingContract(
        contract_id="voice_routing_contract_001",
        total_entries=len(entries),
        routed_entries=sum(1 for entry in entries if entry.routed),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
