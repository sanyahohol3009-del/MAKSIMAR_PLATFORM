from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_policy_handoff_contract import (
    build_gesture_policy_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.voice_display_handoff_contract import (
    build_voice_display_handoff_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class InteractionExposureEntry:
    exposure_entry_id: str
    interaction_source: str
    exposure_channel: str
    policy_bound: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.exposure_entry_id, "exposure_entry_id")
        _require_non_empty(self.interaction_source, "interaction_source")
        _require_non_empty(self.exposure_channel, "exposure_channel")
        _require_non_empty(self.description, "description")

        if not self.policy_bound:
            raise ValueError(
                "policy_bound must remain true for canonical interaction exposure entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical interaction exposure entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical interaction exposure entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical interaction exposure entries."
            )


@dataclass(frozen=True, slots=True)
class InteractionExposureContract:
    contract_id: str
    total_entries: int
    policy_bound_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[InteractionExposureEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.policy_bound_entries != sum(
            1 for entry in self.entries if entry.policy_bound
        ):
            raise ValueError("policy_bound_entries must match policy_bound count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded interaction exposure count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_interaction_exposure_contract() -> InteractionExposureContract:
    gesture_contract = build_gesture_policy_handoff_contract()
    voice_contract = build_voice_display_handoff_contract()

    entries = (
        InteractionExposureEntry(
            exposure_entry_id="interaction_exposure_001",
            interaction_source=gesture_contract.entries[0].adapter_entry_id,
            exposure_channel="gesture_policy_exposure",
            policy_bound=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical interaction exposure entry for gesture chain.",
        ),
        InteractionExposureEntry(
            exposure_entry_id="interaction_exposure_002",
            interaction_source=voice_contract.entries[0].routing_entry_id,
            exposure_channel="voice_display_exposure",
            policy_bound=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical interaction exposure entry for voice chain.",
        ),
    )

    return InteractionExposureContract(
        contract_id="interaction_exposure_contract_001",
        total_entries=len(entries),
        policy_bound_entries=sum(1 for entry in entries if entry.policy_bound),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
