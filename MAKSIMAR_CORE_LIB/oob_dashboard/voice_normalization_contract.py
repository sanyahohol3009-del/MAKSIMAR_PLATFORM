from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


VoiceCommandKind = Literal[
    "voice_navigation_command",
    "voice_explain_command",
    "voice_queue_command",
]

VoiceNormalizationMode = Literal[
    "voice_normalization_ready",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VoiceNormalizationEntry:
    normalization_entry_id: str
    raw_command_id: str
    voice_command_kind: VoiceCommandKind
    transcript_normalized: bool
    structurally_valid: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.normalization_entry_id, "normalization_entry_id")
        _require_non_empty(self.raw_command_id, "raw_command_id")
        _require_non_empty(self.description, "description")

        if not self.transcript_normalized:
            raise ValueError(
                "transcript_normalized must remain true for canonical voice normalization entries."
            )
        if not self.structurally_valid:
            raise ValueError(
                "structurally_valid must remain true for canonical voice normalization entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical voice normalization entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical voice normalization entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical voice normalization entries."
            )


@dataclass(frozen=True, slots=True)
class VoiceNormalizationContract:
    contract_id: str
    mode: VoiceNormalizationMode
    total_entries: int
    normalized_entries: int
    valid_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VoiceNormalizationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.normalized_entries != sum(
            1 for entry in self.entries if entry.transcript_normalized
        ):
            raise ValueError("normalized_entries must match transcript_normalized count.")
        if self.valid_entries != sum(
            1 for entry in self.entries if entry.structurally_valid
        ):
            raise ValueError("valid_entries must match structurally_valid count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded voice normalization count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_voice_normalization_contract() -> VoiceNormalizationContract:
    entries = (
        VoiceNormalizationEntry(
            normalization_entry_id="voice_normalization_001",
            raw_command_id="raw_voice_command_001",
            voice_command_kind="voice_navigation_command",
            transcript_normalized=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical normalized voice navigation command entry.",
        ),
        VoiceNormalizationEntry(
            normalization_entry_id="voice_normalization_002",
            raw_command_id="raw_voice_command_002",
            voice_command_kind="voice_explain_command",
            transcript_normalized=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical normalized voice explain command entry.",
        ),
        VoiceNormalizationEntry(
            normalization_entry_id="voice_normalization_003",
            raw_command_id="raw_voice_command_003",
            voice_command_kind="voice_queue_command",
            transcript_normalized=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical normalized voice queue command entry.",
        ),
    )

    return VoiceNormalizationContract(
        contract_id="voice_normalization_contract_001",
        mode="voice_normalization_ready",
        total_entries=len(entries),
        normalized_entries=sum(1 for entry in entries if entry.transcript_normalized),
        valid_entries=sum(1 for entry in entries if entry.structurally_valid),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
